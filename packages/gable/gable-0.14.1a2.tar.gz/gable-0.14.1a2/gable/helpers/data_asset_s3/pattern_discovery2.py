import calendar
import os
import re
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Optional, Union
from urllib.parse import quote, unquote

from botocore.exceptions import ClientError
from gable.helpers.data_asset_s3.logger import log_debug, log_error, log_trace
from gable.helpers.data_asset_s3.path_pattern_manager import (
    DATE_PLACEHOLDER_TO_REGEX,
    DAY_REGEX,
    HOUR_REGEX,
    MINUTE_REGEX,
    MONTH_REGEX,
    YEAR_REGEX,
    PathPatternManager,
)
from gable.helpers.logging import log_execution_time
from mypy_boto3_s3 import S3Client


class SUPPORTED_FILE_TYPES(Enum):
    CSV = ".csv"
    JSON = ".json"
    PARQUET = ".parquet"


SUPPORTED_FILE_TYPES_SET = set({file_type.value for file_type in SUPPORTED_FILE_TYPES})

DATE_PART_DELIMITERS = "[-_:]{0,2}"
FULL_DATE_MINUTE_REGEX = f"({YEAR_REGEX}){DATE_PART_DELIMITERS}({MONTH_REGEX}){DATE_PART_DELIMITERS}({DAY_REGEX}){DATE_PART_DELIMITERS}({HOUR_REGEX}){DATE_PART_DELIMITERS}({MINUTE_REGEX})"
FULL_DATE_HOUR_REGEX = f"({YEAR_REGEX}){DATE_PART_DELIMITERS}({MONTH_REGEX}){DATE_PART_DELIMITERS}({DAY_REGEX}){DATE_PART_DELIMITERS}({HOUR_REGEX})"
FULL_DATE_DAY_REGEX = f"({YEAR_REGEX}){DATE_PART_DELIMITERS}({MONTH_REGEX}){DATE_PART_DELIMITERS}({DAY_REGEX})"
FULL_DATE_REGEXES = [
    FULL_DATE_MINUTE_REGEX,
    FULL_DATE_HOUR_REGEX,
    FULL_DATE_DAY_REGEX,
]


class DATETIME_DIRECTORY_TYPE(Enum):
    YEAR = YEAR_REGEX
    MONTH = MONTH_REGEX
    DAY = DAY_REGEX
    HOUR = HOUR_REGEX
    MINUTE = MINUTE_REGEX
    FULL_MINUTE = FULL_DATE_MINUTE_REGEX
    FULL_HOUR = FULL_DATE_HOUR_REGEX
    FULL_DAY = FULL_DATE_DAY_REGEX


@log_execution_time
def discover_patterns_from_s3_bucket(
    client: S3Client,
    bucket_name: str,
    start_date: datetime,
    end_date: Optional[datetime] = None,
    include: Optional[list[str]] = None,
    files_per_directory: int = 1000,
    **kwargs,
) -> Dict[str, dict[str, Optional[datetime]]]:
    """
    Discover patterns in an S3 bucket.

    Args:
        bucket (str): S3 bucket.
        files_per_directory (int, optional): Number of files per directory. Defaults to 1000.
        **kwargs:
            include: list of prefixes to include. (TODO: change to be pattern instead of just prefix)
            TODO: add exclude as well
            lookback_days: int, number of days to look back from the latest day in the list of paths. For example
                if the latest path is 2024/01/02, and lookback_days is 4, then the paths return will have
                2024/01/02, 2024/01/01, 2023/12/31, and 2023/12/30
    Returns:
        list[str]: List of patterns.
    """
    log_trace("Starting pattern discovery in bucket: {}", bucket_name)
    _validate_bucket_exists(client, bucket_name)
    path_manager = PathPatternManager()

    _discover_file_paths_from_s3_bucket(
        client,
        path_manager,
        bucket_name,
        "",
        start_date=start_date,
        end_date=end_date,
        max_ls_results=files_per_directory,
        include=include,
    )
    return path_manager.get_pattern_to_actual_paths()


def _discover_file_paths_from_s3_bucket(
    client: S3Client,
    path_manager: PathPatternManager,
    bucket: str,
    prefix: str,
    start_date: datetime,
    end_date: Optional[datetime] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    max_ls_results=1000,
    include: Optional[list[str]] = None,
):
    """
    Discover patterns in an S3 bucket.

    Args:
        client: S3 client.
        bucket (str): S3 bucket.
        prefix (str): Prefix.
        start_date (datetime): The furthest back in time we'll crawl to discover patterns
        end_date (datetime, optional): The most recent point in time we'll crawl to discover patterns. Defaults to None indicating "now".
        year (int, optional): The year if we're in a year directory. Defaults to None.
        month (int, optional): The month if we're in a month directory. Defaults to None.
        day (int, optional): The day if we're in a day directory. Defaults to None.
        hour (int, optional):  The hour if we're in an hour directory. Defaults to None.
        minute (int, optional): The minute if we're in a minute directory. Defaults to None.
        max_ls_results (int, optional): Maximum number of results to return when listing items in a prefix. Defaults to 1000.
    """
    if (
        include
        and len(include) > 0
        and not any([incl in prefix or prefix in incl for incl in include])
    ):
        return
    results: list[str] = []
    try:
        files = _list_files(client, bucket, prefix, max_ls_results)

        # If we're in a day, hour, or minute folder, check for files and add them regardless of the name
        if files and any([day, hour, minute]):
            new_patterns = path_manager.add_filepaths(files)
            if new_patterns:
                log_trace(f"({prefix})\tDiscovered {new_patterns} new pattern(s)")
            else:
                log_trace(f"({prefix})\tNo new pattern(s)")
        elif files:
            # Otherwise, list files and check to see if they have a datetime in them. This catches files like
            # data/shipments_2024-01-01.csv
            datetime_files = [
                f
                for f in files
                if any(map(lambda x: re.search(x, f) is not None, FULL_DATE_REGEXES))
            ]
            # For each file, extract the year, month, day, hour, minute and verify it falls within the start
            # and end date
            datetime_files_to_add = []
            for f in datetime_files:
                success, _year, _month, _day, _hour, _minute = (
                    _get_ymdhm_from_datetime_filename(os.path.basename(f))
                )
                if success and _is_within_look_back_window(
                    start_date, end_date, _year, _month, _day, _hour, _minute
                ):
                    datetime_files_to_add.append(f)
            new_patterns = path_manager.add_filepaths(datetime_files_to_add)
            if new_patterns:
                log_trace(f"({prefix})\tDiscovered {new_patterns} new pattern(s)")
            else:
                log_trace(f"({prefix})\tNo new pattern(s)")

        directories = _list_directories(client, bucket, prefix, max_ls_results)
        grouped_datetime_directories = _group_datetime_directories_by_type(
            directories, year, month, day, hour, minute
        )
        # Split out the non-datetime directories from the datetime directories
        non_datetime_directories = grouped_datetime_directories.pop(None, [])
        # Recursively traverse all of the non-datetime directories, but first, another safety check...
        if len(non_datetime_directories) > 0 and _check_for_alpha_difference(
            non_datetime_directories
        ):
            for dir in non_datetime_directories:
                _discover_file_paths_from_s3_bucket(
                    client,
                    path_manager,
                    bucket,
                    os.path.join(prefix, dir) + "/",
                    start_date=start_date,
                    end_date=end_date,
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    max_ls_results=max_ls_results,
                    include=include,
                )

        elif len(non_datetime_directories) > 0:
            log_debug(
                f"Found non-datetime directories with no alphabetical difference in {bucket}/{prefix}, (example {non_datetime_directories[0]}) skipping further traversal",
            )
        # Now handle the datetime directories
        for (
            datetime_directory_type,
            datetime_directories,
        ) in grouped_datetime_directories.items():
            if datetime_directory_type is not None and len(datetime_directories) > 0:
                # Sort the directories in reverse order so we can break out when we hit the first
                # datetime outside of the start_date
                datetime_directories.sort(reverse=True)
                for datetime_directory in datetime_directories:
                    success, _year, _month, _day, _hour, _minute = (
                        _get_ymdhm_from_datetime_directory(
                            datetime_directory_type,
                            datetime_directory,
                            year,
                            month,
                            day,
                            hour,
                            minute,
                        )
                    )
                    if success and _is_within_look_back_window(
                        start_date, end_date, _year, _month, _day, _hour, _minute
                    ):
                        _discover_file_paths_from_s3_bucket(
                            client,
                            path_manager,
                            bucket,
                            os.path.join(prefix, datetime_directory) + "/",
                            start_date=start_date,
                            end_date=end_date,
                            year=_year,
                            month=_month,
                            day=_day,
                            hour=_hour,
                            minute=_minute,
                            max_ls_results=max_ls_results,
                            include=include,
                        )
                    elif not success:
                        log_debug(
                            f"Failed to parse datetime directory {datetime_directory} in {bucket}/{prefix}, skipping further traversal",
                        )

    except Exception as e:
        log_error("Failed during pattern discovery in {}: {}", bucket, str(e))
        raise
    return results


def _is_within_look_back_window(
    start_date: datetime,
    end_date: Optional[datetime],
    year: Optional[int],
    month: Optional[int],
    day: Optional[int],
    hour: Optional[int],
    minute: Optional[int],
) -> bool:
    # If we're looking at a year directory, we only need to check the year
    if year is not None and not any([month, day, hour, minute]):
        return year >= start_date.year
    # If we're looking at a month directory, trim the start and end dates to the month
    # for the comparison
    if year is not None and month is not None and not any([day, hour, minute]):
        start_date_month = datetime(start_date.year, start_date.month, 1)
        end_date_month = (
            datetime(end_date.year, end_date.month, 1) if end_date else None
        )
        return datetime(year, month, 1) >= start_date_month and (
            end_date_month is None or datetime(year, month, 1) <= end_date_month
        )
    # Otherwise we have at least year, month, day - hour and minute are filled
    # in with 0 if not present
    if year and month and day:
        f_dt = datetime(year, month, day, hour or 0, minute or 0, 0)
        if f_dt >= start_date and (end_date is None or f_dt <= end_date):
            return True
    return False


def _get_ymdhm_from_datetime_directory(
    datetime_directory_type: DATETIME_DIRECTORY_TYPE,
    directory: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    min: Optional[int] = None,
) -> tuple[
    bool, Optional[int], Optional[int], Optional[int], Optional[int], Optional[int]
]:
    directory = super_unquote(directory).rstrip("/")
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.YEAR:
        return True, int(directory), None, None, None, None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.MONTH:
        return True, year, int(directory), None, None, None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.DAY:
        return True, year, month, int(directory), None, None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.HOUR:
        return True, year, month, day, int(directory), None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.MINUTE:
        return True, year, month, day, hour, int(directory)
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_MINUTE:
        matches = re.match(FULL_DATE_MINUTE_REGEX, directory)
        if matches is None:
            return False, None, None, None, None, None
        return (
            True,
            int(matches.group(1)),
            int(matches.group(2)),
            int(matches.group(3)),
            int(matches.group(4)),
            int(matches.group(5)),
        )
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_HOUR:
        matches = re.match(FULL_DATE_HOUR_REGEX, directory)
        if matches is None:
            return False, None, None, None, None, None
        return (
            True,
            int(matches.group(1)),
            int(matches.group(2)),
            int(matches.group(3)),
            int(matches.group(4)),
            None,
        )
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_DAY:
        matches = re.match(FULL_DATE_DAY_REGEX, directory)
        if matches is None:
            return False, None, None, None, None, None
        return (
            True,
            int(matches.group(1)),
            int(matches.group(2)),
            int(matches.group(3)),
            None,
            None,
        )
    return False, None, None, None, None, None


def _get_ymdhm_from_datetime_filename(
    directory: str,
) -> tuple[
    bool, Optional[int], Optional[int], Optional[int], Optional[int], Optional[int]
]:
    directory = super_unquote(directory).rstrip("/")
    search_results = re.search(FULL_DATE_MINUTE_REGEX, directory)
    if search_results:
        return (
            True,
            int(search_results.group(1)),
            int(search_results.group(2)),
            int(search_results.group(3)),
            int(search_results.group(4)),
            int(search_results.group(5)),
        )
    search_results = re.search(FULL_DATE_HOUR_REGEX, directory)
    if search_results:
        return (
            True,
            int(search_results.group(1)),
            int(search_results.group(2)),
            int(search_results.group(3)),
            int(search_results.group(4)),
            None,
        )
    search_results = re.search(FULL_DATE_DAY_REGEX, directory)
    if search_results:
        return (
            True,
            int(search_results.group(1)),
            int(search_results.group(2)),
            int(search_results.group(3)),
            None,
            None,
        )
    return False, None, None, None, None, None


def _check_for_alpha_difference(directories: list[str]) -> bool:
    """
    Checks to see if there is a difference in the list of directory names if all numbers are removed. This is used
    to detect a folder pattern we don't understand, but that has a consistent pattern. We don't want to traverse these
    directories, or we may end up iterating over a large number of directories and consider them all separate data assets.

    Example: ["0000001", "0000002", "0000003"] would return False, because the only difference is the numbers

    Args:
        list[str]: List of strings.

    Returns:
        bool: True if there is a difference in alphabetical order, False otherwise.
    """
    # Edge case: if there's only one directory just return True
    if len(directories) == 1:
        return True
    stripped_directories = [re.sub(r"\d", "", directory) for directory in directories]
    return len(set(stripped_directories)) > 1


def _group_datetime_directories_by_type(
    directories: list[str], year=None, month=None, day=None, hour=None, minute=None
) -> dict[Optional[DATETIME_DIRECTORY_TYPE], list[str]]:
    directory_groups = {}
    for directory in directories:
        directory_type = _get_datetime_directory_type(
            directory, year, month, day, hour, minute
        )

        if directory_type not in directory_groups:
            directory_groups[directory_type] = []
        directory_groups[directory_type].append(directory)
    return directory_groups


def _get_datetime_directory_type(
    directory: str, year=None, month=None, day=None, hour=None, minute=None
) -> Optional[DATETIME_DIRECTORY_TYPE]:
    # Trim the directory to remove any trailing slashes
    directory = super_unquote(directory).rstrip("/")
    # If we're already in a minute directory, don't go any deeper
    if minute is not None:
        return None
    # Otherwise check if the directory matches the next logical datetime part regex
    if (
        hour is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.MINUTE.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.MINUTE
    if (
        day is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.HOUR.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.HOUR
    if (
        month is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.DAY.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.DAY
    if (
        year is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.MONTH.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.MONTH
    # At this point we're not in any sort of datetime directory, so check if it's a year directory, or a full date directory
    if re.fullmatch(DATETIME_DIRECTORY_TYPE.YEAR.value, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.YEAR
    if re.match(FULL_DATE_MINUTE_REGEX, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_MINUTE
    if re.match(FULL_DATE_HOUR_REGEX, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_HOUR
    if re.match(FULL_DATE_DAY_REGEX, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_DAY
    return None


def _list_directories(
    client: S3Client, bucket: str, prefix: str, max_ls_results: int = 1000
) -> list[str]:
    """
    List all directories in an S3 bucket. Returns only the directory names, not the full path.

    Args:
        bucket_name (str): S3 bucket.
        prefix (str): Prefix. This is used for recursive calls and differs from kwargs["include"] which is a configuration option.

    Returns:
        list[str]: List of directories.
    """
    return list(
        map(
            lambda x: x.rstrip("/").split("/")[-1],
            filter(
                None,
                map(
                    lambda x: x.get("Prefix"),
                    client.list_objects_v2(
                        Bucket=bucket,
                        Prefix=prefix,
                        Delimiter="/",
                        MaxKeys=max_ls_results,
                    ).get("CommonPrefixes", []),
                ),
            ),
        )
    )


def _list_files(
    client: S3Client, bucket: str, prefix: str, max_ls_results: int = 1000
) -> list[str]:
    """
    List all directories in an S3 bucket.

    Args:
        bucket_name (str): S3 bucket.
        prefix (str): Prefix. This is used for recursive calls and differs from kwargs["include"] which is a configuration option.

    Returns:
        list[str]: List of directories.
    """
    contents = client.list_objects_v2(
        Bucket=bucket, Prefix=prefix, Delimiter="/", MaxKeys=max_ls_results
    ).get("Contents", [])
    return list(
        filter(
            is_supported_file_type,
            filter(
                None,
                map(
                    lambda x: x.get("Key"),
                    contents,
                ),
            ),
        )
    )


def is_supported_file_type(file_path: str) -> bool:
    """
    Check if the file type is supported.

    Args:
        file_path (str): File path.

    Returns:
        bool: True if the file type is supported, False otherwise.
    """
    return any(
        [file_path.endswith(file_type) for file_type in SUPPORTED_FILE_TYPES_SET]
    )


def super_unquote(s: str):
    new_s, _ = super_unquote_n(s)
    return new_s


def super_unquote_n(s: str):
    if s == unquote(s):
        return s, 0
    old_s = s
    s = unquote(s)
    quote_count = 1
    while s != old_s:
        old_s = s
        s = unquote(s)
        quote_count += 1
    return s, quote_count


def super_quote(s: str, count):
    for _ in range(count):
        s = quote(s)
    return s


# @log_execution_time
# def discover_filepaths_from_patterns(
#     client, bucket_name: str, patterns: list[str], file_count: int = 1000, **kwargs
# ) -> list[str]:
#     """
#     Discover filepaths in an S3 bucket from patterns.

#     Args:
#         bucket_name (str): S3 bucket.
#         patterns (list[str]): List of patterns.

#     Returns:
#         list[str]: List of filepaths.
#     """
#     log_trace("Starting filepath discovery from patterns in {}", bucket_name)
#     filepaths: set[str] = set()
#     for pattern in patterns:
#         log_trace("Discovering filepaths for pattern: {}", pattern)
#         for filepath in _get_latest_filepaths_from_pattern(
#             client, bucket_name, pattern, file_count, **kwargs
#         ):
#             filepaths.add(filepath)
#     log_trace("Completed filepath discovery from patterns in {}", bucket_name)
#     return list(filepaths)


# def discover_filepaths_by_date_range(
#     client,
#     bucket_name: str,
#     base_pattern: str,
#     start_date: str,
#     end_date: str = "",
#     file_count: int = 1,
# ) -> list[str]:
#     """
#     Discover filepaths in an S3 bucket that match a pattern for a given date.
#     Args:
#         client: S3 client.
#         bucket_name (str): name of S3 bucket.
#         base_pattern (str): The base pattern with placeholders.
#         date_str (str): Date in 'YYYY-MM-DD' format.
#         file_count (int): Number of latest files to retrieve.
#     Returns:
#         list[str]: List of filepaths that match the date-injected pattern.
#     """
#     start_range_pattern = replace_date_placeholders(base_pattern, start_date)
#     end_range_pattern = replace_date_placeholders(base_pattern, end_date)
#     patterns = [start_range_pattern, end_range_pattern]
#     filepaths: list[str] = []
#     for pattern in patterns:
#         filepaths.extend(
#             _get_latest_filepaths_from_pattern(client, bucket_name, pattern, file_count)
#         )
#     return filepaths


# def discover_most_recent_filepath_by_date(
#     client, bucket_name: str, base_pattern: str, date_str: str, file_count: int = 1
# ) -> list[str]:
#     """
#     Discover the most recent filepath in an S3 bucket that matches a pattern for a given date.

#     Args:
#         client: S3 client.
#         bucket_name (str): Name of the S3 bucket.
#         base_pattern (str): The base pattern with placeholders for the date.
#         date_str (str): Date in 'YYYY-MM-DD' format to search for files.
#         file_count (int): Maximum number of latest files to retrieve.

#     Returns:
#         Optional[str]: The most recent file path or None if no files are found.
#     """
#     pattern = replace_date_placeholders(base_pattern, date_str)
#     return _get_latest_filepaths_from_pattern(client, bucket_name, pattern, file_count)


# @log_execution_time
# def _get_latest_filepaths_from_pattern(
#     client, bucket_name: str, pattern: str, file_count: int, **kwargs
# ) -> list[str]:
#     """
#     Get the n latest files from a DARN pattern.

#     Args:
#         bucket_name (str): S3 bucket.
#         pattern (str): pattern.
#         count (int): Number of files to get.

#     Returns:
#         list[str]: list of filepaths
#     """
#     optimized_prefix = _generate_optimized_prefix(pattern)
#     files = _list_files(client, bucket_name, file_count, optimized_prefix, **kwargs)
#     files = sorted(files, key=lambda x: x["LastModified"], reverse=True)
#     return [file["Key"] for file in files[:file_count]]


# def _generate_optimized_prefix(pattern: str) -> str:
#     optimized_prefix_parts = []
#     now = datetime.now()
#     regex_replacements = [
#         (r"{YYYY}", now.strftime("%Y")),
#         (r"{MM}", now.strftime("%m")),
#         (r"{DD}", now.strftime("%d")),
#         (r"{YYYY-MM-DD}", now.strftime("%Y-%m-%d")),
#         (r"{YYYY-MM-DD.+}.*", now.strftime("%Y-%m-%d")),
#         (r"{YYYYMMDD}", now.strftime("%Y%m%d")),
#         (r"{YYYYMMDD.+}.*", now.strftime("%Y%m%d")),
#     ]
#     for part in pattern.split("/"):
#         found_match = False
#         cannot_optimize_further = False
#         for regex, replacement in regex_replacements:
#             if re.match(".*" + regex, part):
#                 found_match = True
#                 replacement_part = re.sub(regex, replacement, part)
#                 optimized_prefix_parts.append(replacement_part)
#                 cannot_optimize_further = regex.endswith(".*")
#                 break
#         if not found_match:
#             if "{" in part:  # no match found, so we can't optimize any further
#                 break
#             else:
#                 optimized_prefix_parts.append(part)
#         elif cannot_optimize_further:
#             break
#     return "/".join(optimized_prefix_parts)


def _discover_patterns_from_filepaths(
    filepaths: list[str],
) -> Dict[str, dict[str, Optional[datetime]]]:
    """
    Discover patterns in a list of filepaths.

    Args:
        filepaths (list[str]): List of filepaths.

    Returns:
        Iterable[str]: List of patterns.
    """
    log_trace("Adding filepaths to PathPatternManager")
    path_manager = PathPatternManager()
    path_manager.add_filepaths(filepaths)
    return path_manager.get_pattern_to_actual_paths()


# def _list_files(
#     client, bucket_name: str, files_per_directory: int, prefix: str, **kwargs
# ) -> list[dict]:
#     """
#     List objects in an S3 bucket.

#     Args:
#         bucket_name (str): S3 bucket.
#         files_per_directory: (int, optional): Number of files per directory. Defaults to all files
#         prefix (str): Prefix. For all files, supply an empty string.
#         **kwargs:
#             include: list of prefixes to include. (TODO: change to be pattern instead just prefix)
#             TODO: add exclude as well
#             lookback_days: int, number of days to look back for recent patterns.
#     Returns:
#         list[dict]: mapping of file names to contents.
#     """
#     _validate_bucket_exists(client, bucket_name)
#     try:
#         log_debug("Listing files in {}: prefix={}", bucket_name, prefix)
#         dirpaths = _list_all_dirpaths(client, bucket_name, prefix, **kwargs)
#         log_trace("Listed directories to crawl: {}", dirpaths)
#         files: list[dict[str, dict]] = []
#         for dirpath in dirpaths:
#             files.extend(
#                 _list_all_files_paginated(
#                     client,
#                     bucket_name,
#                     files_per_directory,
#                     dirpath,
#                 )
#             )
#         log_debug("Listed files in {}: prefix={}", bucket_name, prefix)
#         return files
#     except Exception as e:
#         log_error("Failed to list files in {}: {}", bucket_name, str(e))
#         return []


# def _list_all_files_paginated(
#     client, bucket_name: str, max_files: int, prefix: str = ""
# ) -> list[dict[str, dict]]:
#     """
#     List objects in an S3 bucket.

#     Args:
#         bucket_name (str): S3 bucket.
#         max_files (int): Maximum number of files to list.
#         prefix (str, optional): Prefix. Defaults to None.
#     Returns:
#         dict[str, object]: mapping of file names to contents.
#     """
#     log_trace(
#         "Starting to paginate files in bucket: {} with prefix: {}", bucket_name, prefix
#     )
#     paginator = client.get_paginator("list_objects_v2")
#     files: list[dict[str, dict]] = []
#     for page in paginator.paginate(
#         Bucket=bucket_name,
#         Prefix=prefix,
#         PaginationConfig={"MaxItems": max_files},
#     ):
#         for obj in page.get("Contents", []):
#             files.append(obj)
#     log_trace("Completed listing files, total files gathered: {}", len(files))
#     return files


#     # paginator = client.get_paginator("list_objects_v2")
#     # pagination_result = paginator.paginate(
#     #     Bucket=bucket_name, Delimiter="/", Prefix=prefix
#     # )
#     # search_result = _extract_prefixes_from_results(
#     #     pagination_result.search("CommonPrefixes") or []
#     # )
#     # content_result = pagination_result.search("Contents")
#     # dirpaths = []
#     # log_trace("Listing dirpaths for prefix: {}", prefix)
#     # prefix_in_include = (
#     #     len(include) > 0 and any([incl in prefix for incl in include])
#     # ) or len(include) == 0
#     # file_exists = next(content_result, None) is not None
#     # if prefix_in_include and file_exists:
#     #     # if the prefix is in the include list, and there are files at the prefix location, then the prefix is a dirpath
#     #     dirpaths.append(prefix)

#     # common_prefixes = (
#     #     _trim_recent_patterns(search_result, include, lookback_days)
#     #     if trim_recent_patterns
#     #     else search_result
#     # )
#     # for next_prefix in common_prefixes:
#     #     if next_prefix is None:
#     #         # once next_prefix is none, we've hit the bottom of the dir tree, so the current prefix arg is a full prefix
#     #         if prefix not in dirpaths:
#     #             # multiple paginations can return the same prefix, so avoid duplication
#     #             dirpaths.append(prefix)
#     #     else:
#     #         dirpaths.extend(
#     #             _list_all_dirpaths(client, bucket_name, next_prefix, **kwargs)
#     #         )
#     # log_trace(
#     #     "Completed directory listing under prefix {}, total directories found: {}",
#     #     prefix,
#     #     len(dirpaths),
#     # )
#     # return dirpaths


# def _extract_prefixes_from_results(
#     results: list[Union[dict, None]]
# ) -> list[Union[str, None]]:
#     return [(result or {}).get("Prefix", None) for result in results]


# def _strip_slashes(path: str) -> str:
#     return path.strip("/")


# def _trim_recent_patterns(
#     paths: list[Union[str, None]], include: list[str], lookback_days: int
# ) -> list[Union[str, None]]:
#     """
#     Trim recent patterns from a list of paths in order to get a reduced set of paths for optimization.
#     lookback_days is used to determine how many days back to look, from the latest day in the list of paths. For example
#     if the latest path is 2024/01/02, and lookback_days is 4, then the paths return will have
#     2024/01/02, 2024/01/01, 2023/12/31, and 2023/12/30
#     """
#     prefixes = set(
#         [
#             os.path.join("", *_strip_slashes(path or "").split("/")[:-1])
#             for path in paths
#         ]
#     )
#     if len(prefixes) == 0:
#         return []
#     if len(prefixes) > 1:
#         raise ValueError(
#             "Optimization does not make sense for multiple prefixes, they should be separate calls to this function"
#         )

#     suffixes = [
#         None if path is None else _strip_slashes(path).split("/")[-1] for path in paths
#     ]
#     prefix = next(iter(prefixes))
#     result_suffixes: list[Union[str, None]] = []
#     max_num_type = None
#     max_num, original_max_num_str = None, None
#     max_date, original_max_date_format = None, None
#     suffix_to_quote_count = {}
#     for suffix in suffixes:
#         proposed_path = os.path.join(prefix, suffix or "")
#         if len(include) > 0 and any(
#             [incl.startswith(proposed_path) for incl in include]
#         ):
#             result_suffixes.append(suffix)
#         elif suffix:
#             if re.match(
#                 rf".*/({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})/?$", prefix
#             ) and re.match(HOUR_REGEX, suffix):
#                 max_num_type = "hour"
#             elif re.match(
#                 rf".*/({YEAR_REGEX})/({MONTH_REGEX})/?$", prefix
#             ) and re.match(DAY_REGEX, suffix):
#                 max_num_type = "day"

#             if len(suffix) <= 4 and suffix.isdigit():
#                 num = int(suffix)
#                 if max_num is None or num > max_num:
#                     max_num = num
#                     original_max_num_str = suffix
#                 else:
#                     result_suffixes.append(None)
#             else:
#                 found_match = False
#                 for reg, format in [
#                     # return same order as in DATE_PLACEHOLDER_TO_REGEX
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYY-MM-DD:HH:mm}"], "%Y-%m-%d:%H:%M"),
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD:HH:mm}"], "%Y%m%d:%H:%M"),
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYY-MM-DD:HH}"], "%Y-%m-%d:%H"),
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD_HH}"], "%Y%m%d_%H"),
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD:HH}"], "%Y%m%d:%H"),
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDDHH}"], "%Y%m%d%H"),
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYY-MM-DD}"], "%Y-%m-%d"),
#                     (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD}"], "%Y%m%d"),
#                 ]:
#                     decoded = suffix
#                     quote_count = 0
#                     while decoded != (decoded := unquote(decoded)):
#                         quote_count += 1
#                     suffix_to_quote_count[decoded] = quote_count
#                     if re.match(reg, decoded):
#                         try:
#                             date = datetime.strptime(decoded, format)
#                             if max_date is None or date > max_date:
#                                 max_date = date
#                                 original_max_date_format = format
#                                 found_match = True
#                         except ValueError as e:
#                             log_error(
#                                 "Failed to parse date {} with {}: {}",
#                                 decoded,
#                                 format,
#                                 str(e),
#                             )
#                         break
#                 if not found_match:
#                     result_suffixes.append(suffix)
#         else:
#             result_suffixes.append(None)

#     extra_paths = []
#     if max_num is not None:
#         if max_num_type == "hour":
#             if matches := re.match(
#                 rf".*/({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})/?$", prefix
#             ):
#                 year, month, day = matches.groups()
#                 latest_datetime = datetime(int(year), int(month), int(day), max_num)
#                 for day in range(lookback_days + 1):
#                     for hour in range(24):
#                         assembled_datetime = latest_datetime - timedelta(
#                             days=day, hours=hour
#                         )
#                         extra_paths.append(
#                             re.sub(
#                                 rf"/({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})",
#                                 f"/{assembled_datetime.year:04d}/{assembled_datetime.month:02d}/{assembled_datetime.day:02d}",
#                                 prefix,
#                             )
#                             + f"/{assembled_datetime.hour:02d}/"
#                         )
#         elif max_num_type == "day":
#             if matches := re.match(f".*/({YEAR_REGEX})/({MONTH_REGEX})/?$", prefix):
#                 year, month = matches.groups()
#                 latest_datetime = datetime(int(year), int(month), max_num)
#                 for days in range(lookback_days + 1):
#                     assembled_datetime = latest_datetime - timedelta(days=days)
#                     # there's no guarantee that these paths exist from the listing, but if they don't exist they just won't be read and parsed
#                     extra_paths.append(
#                         re.sub(
#                             rf"/({YEAR_REGEX})/({MONTH_REGEX})",
#                             f"/{assembled_datetime.year:04d}/{assembled_datetime.month:02d}",
#                             prefix,
#                         )
#                         + f"/{assembled_datetime.day:02d}/"
#                     )
#         else:
#             result_suffixes.append(original_max_num_str)
#     if max_date is not None and original_max_date_format is not None:
#         for day in range(lookback_days + 1):
#             if "%M" in original_max_date_format:
#                 # fill in down to minute granularity
#                 for hour in range(24):
#                     for minute in range(60):
#                         result_suffixes.append(
#                             (
#                                 max_date
#                                 - timedelta(days=day, hours=hour, minutes=minute)
#                             ).strftime(original_max_date_format)
#                         )
#             elif "%H" in original_max_date_format:
#                 # fill in down to hour granularity
#                 for hour in range(24):
#                     result_suffixes.append(
#                         (max_date - timedelta(days=day, hours=hour)).strftime(
#                             original_max_date_format
#                         )
#                     )
#             else:  # just day granularity
#                 result_suffixes.append(
#                     (max_date - timedelta(days=day)).strftime(original_max_date_format)
#                 )

#     return [
#         (
#             None
#             if suffix is None
#             else os.path.join(
#                 prefix, _quote_n_times(suffix, suffix_to_quote_count.get(suffix, 0))
#             )
#             + "/"
#         )
#         for suffix in result_suffixes
#     ] + extra_paths


# def _quote_n_times(s: str, n: int) -> str:
#     for _ in range(n):
#         s = quote(s)
#     return s


def _validate_bucket_exists(client: S3Client, bucket_name: str) -> None:
    log_trace("Validating existence of bucket: {}", bucket_name)
    try:
        client.head_bucket(Bucket=bucket_name)
        log_trace("Bucket exists: {}", bucket_name)
    except client.exceptions.ClientError as e:
        if isinstance(e, ClientError):
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                print(f"Bucket {bucket_name} does not exist.")
                log_error("Bucket does not exist for {}: {}", bucket_name, str(e))
            elif error_code == 403:
                print(f"Access to bucket {bucket_name} is forbidden.")
                log_error(
                    "Access to bucket is forbidden for {}: {}", bucket_name, str(e)
                )
        raise ValueError(
            f"Bucket {bucket_name} does not exist or is not accessible. Check that AWS credentials are set up correctly."
        )


# def replace_date_placeholders(pattern: str, date_str: str = "") -> str:
#     """
#     Replace date placeholders in the pattern with the provided date string or today's date if not provided.

#     Args:
#         pattern (str): The pattern containing placeholders.
#         date_str (str, optional): Date in 'YYYY-MM-DD' format to inject into the pattern. Defaults to today's date.

#     Returns:
#         str: The pattern with date placeholders replaced.
#     """
#     # Use the current date if no date string is provided
#     if date_str == "":
#         date = datetime.now()
#     else:
#         date = datetime.strptime(date_str, "%Y-%m-%d")

#     date = datetime.strptime(date_str, "%Y-%m-%d")
#     year = date.strftime("%Y")
#     month = date.strftime("%m")
#     day = date.strftime("%d")

#     # Replace the placeholders within the curly braces
#     pattern = (
#         pattern.replace("{YYYY}", year).replace("{MM}", month).replace("{DD}", day)
#     )
#     pattern = pattern.replace("{YYYY-MM-DD}", f"{year}-{month}-{day}")

#     # Replace placeholders without curly braces if directly included in the string
#     pattern = pattern.replace("{YYYYMMDD}", f"{year}{month}{day}")
#     pattern = pattern.replace("YYYY", year).replace("MM", month).replace("DD", day)

#     return pattern


def flatten(lists: list):
    return list((item for sublist in lists for item in sublist))
