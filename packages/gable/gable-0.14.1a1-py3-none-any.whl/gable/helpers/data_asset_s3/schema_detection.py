import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Optional, Union

import boto3
import click
import deepdiff
import gable.helpers.data_asset_s3.pattern_discovery2 as pattern_discovery2
import pandas as pd
import s3fs
from click.core import Context as ClickContext
from fastparquet import ParquetFile
from gable.client import CheckDataAssetDetailedResponseUnion, GableClient
from gable.helpers.data_asset_s3 import NativeS3Converter
from gable.helpers.data_asset_s3.path_pattern_manager import (
    DATE_PLACEHOLDER_TO_REGEX,
    PathPatternManager,
)
from gable.helpers.data_asset_s3.pattern_discovery import (
    discover_filepaths_from_patterns,
)
from gable.helpers.data_asset_s3.pattern_discovery2 import SUPPORTED_FILE_TYPES
from gable.helpers.emoji import EMOJI
from gable.helpers.logging import log_execution_time
from gable.openapi import (
    CheckComplianceDataAssetsS3Request,
    CheckDataAssetCommentMarkdownResponse,
    ErrorResponse,
    IngestDataAssetResponse,
    RegisterDataAssetS3Request,
    ResponseType,
    S3Asset,
)
from loguru import logger
from mypy_boto3_s3 import S3Client

NUM_ROWS_TO_SAMPLE = 1000
CHUNK_SIZE = 100
NUM_FILES_TO_SAMPLE = 1


def get_dfs_from_s3_files(
    s3_urls: list[str], s3_opts: Optional[dict] = None
) -> list[tuple[pd.DataFrame, bool]]:
    """
    Read data from given S3 file urls (only CSV, JSON, and parquet currently supported) and return pandas DataFrames.
    Args:
        s3_urls (list[str]): List of S3 URLs.
        s3_opts (dict): S3 storage options. - only needed for tests using moto mocking
    Returns:
        list[tuple[pd.DataFrame, bool]]: List tuple of pandas DataFrames and a boolean indicating if the DataFrame has a predefined schema.
    """
    result = []
    for url in s3_urls:
        if df := read_s3_file(url, s3_opts):
            result.append(df)
    return result


def read_s3_file(
    url: str, s3_opts: Optional[dict] = None
) -> Optional[tuple[pd.DataFrame, bool]]:
    try:
        if url.endswith(SUPPORTED_FILE_TYPES.CSV.value):
            logger.debug(f"Reading from S3 file: {url}")
            return get_csv_df(url, s3_opts), False
        elif url.endswith(SUPPORTED_FILE_TYPES.JSON.value):
            logger.debug(f"Reading from S3 file: {url}")
            df = pd.concat(
                pd.read_json(
                    url,
                    lines=True,
                    chunksize=CHUNK_SIZE,
                    nrows=NUM_ROWS_TO_SAMPLE,
                    storage_options=s3_opts,
                ),
                ignore_index=True,
            )
            return flatten_json(df), False
        elif url.endswith(SUPPORTED_FILE_TYPES.PARQUET.value):
            logger.debug(f"Reading from S3 file: {url}")
            return get_parquet_df(url, s3_opts), True
        else:
            logger.debug(f"Unsupported file format: {url}")
            return None
    except Exception as e:
        # Swallowing exceptions to avoid failing processing other files
        logger.opt(exception=e).error(f"Error reading file {url}: {e}")
        return None


def get_parquet_df(url: str, s3_opts: Optional[dict] = None) -> pd.DataFrame:
    """
    Read Parquet file from S3 and return an empty pandas DataFrame with the schema.
    """
    parquet_file = ParquetFile(url, fs=s3fs.S3FileSystem(**(s3_opts or {})))
    # read default sample size rows in order to compute profile. Only 1 row is needed to compute schema
    return parquet_file.head(NUM_ROWS_TO_SAMPLE)


def get_csv_df(url: str, s3_opts: Optional[dict] = None) -> pd.DataFrame:
    """
    Read CSV file from S3 and return a pandas DataFrame. Special handling for CSV files with and without headers.
    """
    df_header = pd.concat(
        pd.read_csv(
            url,
            chunksize=CHUNK_SIZE,
            nrows=NUM_ROWS_TO_SAMPLE,
            storage_options=s3_opts,
        ),
        ignore_index=True,
    )
    df_no_header = pd.concat(
        pd.read_csv(
            url,
            header=None,
            chunksize=CHUNK_SIZE,
            nrows=NUM_ROWS_TO_SAMPLE,
            storage_options=s3_opts,
        ),
        ignore_index=True,
    )
    return (
        df_header
        if tuple(df_no_header.dtypes) != tuple(df_header.dtypes)
        else df_no_header
    )


def flatten_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens any nested JSON data to a single column
    {"customerDetails": {"technicalContact": {"email": "...."}}}" => customerDetails.technicalContact.email
    """
    json_struct = json.loads(df.to_json(orient="records"))  # type: ignore
    return pd.json_normalize(json_struct)


def get_s3_client() -> S3Client:
    return boto3.client("s3")


def append_s3_url_prefix(bucket: str, url: str) -> str:
    return "s3://" + bucket + "/" + url if not url.startswith("s3://") else url


def strip_s3_bucket_prefix(bucket: str) -> str:
    return bucket.removeprefix("s3://")


def extract_date_from_pattern(pattern: str) -> Optional[str]:
    """Extract date from pattern using regex."""
    match = re.search(r"\d{4}/\d{2}/\d{2}", pattern)
    return match.group(0) if match else None


def format_deepdiff_output(deepdiff_result):
    """
    Formats the deepdiff output for CLI display.
    """
    formatted_output = []

    # Handle changed values
    values_changed = deepdiff_result.get("values_changed", {})
    if values_changed:
        formatted_output.append("\nChanged values:")
        for key, details in values_changed.items():
            parsed = parse_diff_key(key)
            formatted_output.append(
                f"  - {parsed} Changed from '{details['old_value']}' to '{details['new_value']}'"
            )
    # Handle items added
    items_added = deepdiff_result.get("iterable_item_added", {})
    if items_added:
        formatted_output.append("\nItems added:")
        for key, value in items_added.items():
            formatted_output.append(
                f"  - {key}: Added '{value['name']}' of Type '{value['type']}'"
            )

    # Handle items removed
    items_removed = deepdiff_result.get("iterable_item_removed", {})
    if items_removed:
        formatted_output.append("\nItems removed:")
        for key, value in items_removed.items():
            formatted_output.append(
                f"  - {key}: Removed '{value['name']}' of Type '{value['type']}'"
            )

    return "\n".join(formatted_output)


def extract_date_from_filepath(filepath):
    # This regex assumes the date format in the filepath is something like '2024/04/10'
    match = re.search(DATE_PLACEHOLDER_TO_REGEX["{YYYY}/{MM}/{DD}"], filepath)
    if match:
        return datetime.strptime(match.group(1), "%Y/%m/%d").date()
    return None


def parse_diff_key(key: str) -> str:
    # This regex extracts the index and the attribute being compared
    match = re.search(r"\['fields'\]\[(\d+)\]\['(\w+)'\]", key)
    if match:
        attribute = match.group(2)
        return f"{attribute.capitalize()}"
    return "Unknown field"


def get_schemas_from_files(
    client, bucket: str, pattern, files_urls: list[str]
) -> list[dict]:
    """Retrieve and convert data from S3 into Recap schemas."""
    dfs = get_dfs_from_s3_files(files_urls)
    return [
        NativeS3Converter().to_recap(df, has_schema, pattern) for df, has_schema in dfs
    ]


def compare_schemas(
    schema1: list[dict],
    schema2: list[dict],
    pattern: str,
    first_date: Union[str, None],
    second_date: Union[str, None],
):
    """Compare two sets of schemas and log the differences."""
    for schema_h, schema_t in zip(schema1, schema2):
        diff = deepdiff.DeepDiff(schema_h, schema_t, ignore_order=True)
        if diff:
            formatted_results = format_deepdiff_output(diff)
            logger.info(
                f"\n\nDifferences detected in {pattern} between {first_date} and {second_date}: \n{formatted_results}\n\n"
            )
        else:
            logger.info(
                f"\n\nNo differences detected in {pattern} between {first_date} and {second_date}.\n\n"
            )


def detect_s3_data_assets_history(bucket: str, include: list[str]):
    client = get_s3_client()
    first_pattern = include[0]
    second_pattern = include[1]
    first_date = extract_date_from_pattern(first_pattern)
    second_date = extract_date_from_pattern(second_pattern)
    first_date_files = pattern_discovery2.discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket),
        start_date=datetime(1970, 1, 1),
        end_date=None,
        include=[first_pattern],
    )
    second_date_files = pattern_discovery2.discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket),
        start_date=datetime(1970, 1, 1),
        end_date=None,
        include=[second_pattern],
    )
    all_patterns = list(set(first_date_files.keys()) | set(second_date_files.keys()))
    if not all_patterns:
        raise click.ClickException(
            "No data assets found to compare! Use the --debug or --trace flags for more details."
        )
    for pattern in all_patterns:
        # Retrieve schemas for both dates
        schema_historical = get_schemas_from_files(
            client,
            strip_s3_bucket_prefix(bucket),
            pattern,
            list(first_date_files.get(pattern, {}).keys()),
        )
        schema_today = get_schemas_from_files(
            client,
            strip_s3_bucket_prefix(bucket),
            pattern,
            list(second_date_files.get(pattern, {}).keys()),
        )

        compare_schemas(
            schema_historical, schema_today, first_pattern, first_date, second_date
        )


def detect_s3_data_assets(
    bucket: str,
    lookback_days: int = 1,
    include: Optional[list[str]] = None,
) -> dict[str, dict]:
    """
    Detect data assets in S3 bucket.
    Args:
        bucket (str): S3 bucket name.
        lookback_days (int): Lookback days.
        include (list[str]): List of patterns to include.
    Returns:
        dict[str, dict]: Mapping of asset pattern to schema.
    """
    schemas: dict[str, dict] = {}
    client = get_s3_client()
    patterns_to_urls = pattern_discovery2.discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket),
        start_date=datetime.now() - timedelta(days=lookback_days),
        include=include,
    )
    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda entry: (
                entry[0],
                get_merged_def_from_s3_files(strip_s3_bucket_prefix(bucket), *entry),
            ),
            patterns_to_urls.items(),
        )
        schemas.update(
            {
                pattern: result
                for pattern, result in results
                if result.get("fields", None)
            }
        )
    return schemas


def register_s3_data_assets(
    ctx: ClickContext,
    bucket: str,
    lookback_days: int = 1,
    include: Optional[list[str]] = None,
    dry_run: bool = False,
):
    pattern_to_schema = detect_s3_data_assets(bucket, lookback_days, include)
    if len(pattern_to_schema) == 0:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
        )

    logger.info(
        f"{EMOJI.GREEN_CHECK.value} {len(pattern_to_schema)} S3 data asset(s) found:"
    )

    for pattern, schema in pattern_to_schema.items():
        logger.info(f"Pattern: {pattern}\nSchema: {json.dumps(schema, indent=4)}")

    if dry_run:
        logger.info("Dry run mode. Data asset registration not performed.")
        return (
            IngestDataAssetResponse(message="", registered=[], success=True),
            True,
            200,
        )
    else:
        request = RegisterDataAssetS3Request(
            dry_run=dry_run,
            assets=[
                S3Asset(
                    schema=schema,
                    bucket=bucket,
                    pattern=pattern,
                )
                for pattern, schema in pattern_to_schema.items()
            ],
        )
        # click doesn't let us specify the type of ctx.obj.client in the Context:
        client: GableClient = ctx.obj.client
        return client.post_data_asset_register_s3(request)


def check_compliance_s3_data_assets(
    ctx: ClickContext,
    response_type: ResponseType,
    bucket: str,
    lookback_days: int = 1,
    include: Optional[list[str]] = None,
) -> Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[CheckDataAssetDetailedResponseUnion],
]:
    pattern_to_schema = detect_s3_data_assets(bucket, lookback_days, include)
    if len(pattern_to_schema) == 0:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to check compliance! You can use the --debug or --trace flags for more details.",
        )

    request = CheckComplianceDataAssetsS3Request(
        assets=[
            S3Asset(
                schema=schema,
                bucket=bucket,
                pattern=pattern,
            )
            for pattern, schema in pattern_to_schema.items()
        ],
        responseType=response_type,
    )
    client: GableClient = ctx.obj.client
    return client.post_check_compliance_data_assets_s3(request)


def get_merged_def_from_s3_files(
    bucket: str,
    event_name: str,
    s3_urls: dict[str, datetime],
    num_files_to_sample: int = NUM_FILES_TO_SAMPLE,
) -> dict:
    """
    Get merged definition from given S3 file urls (only CSV, JSON, and parquet currently supported).
    Args:
        bucket (str): S3 bucket name.
        event_name (str): Event name.
        s3_urls (list[str]): List of S3 URLs.
    Returns:
        dict: Merged definition.
    """
    most_recent_urls = [
        url[0]
        for url in sorted(s3_urls.items(), key=lambda x: x[1], reverse=True)[
            :num_files_to_sample
        ]
    ]
    urls = [append_s3_url_prefix(bucket, url) for url in most_recent_urls]
    dfs = get_dfs_from_s3_files(urls)
    return merge_schemas(
        [
            NativeS3Converter().to_recap(df, has_schema, event_name)
            for df, has_schema in dfs
            if len(df.columns) > 0
        ]
    )


def merge_schemas(schemas: list[dict]) -> dict:
    """
    Merge multiple schemas into a single schema.
    Args:
        schemas (list[dict]): List of schemas.
    Returns:
        dict: Merged schema.
    """
    # Dictionary of final fields, will be turned into a struct type at the end
    result_dict: dict[str, dict] = {}
    for schema in schemas:
        if "fields" in schema:
            for field in schema["fields"]:
                field_name = field["name"]
                # If the field is not yet in the result, just add it
                if field_name not in result_dict:
                    result_dict[field_name] = field
                elif field != result_dict[field_name]:
                    # If both types are structs, recursively merge them
                    if (
                        field["type"] == "struct"
                        and result_dict[field_name]["type"] == "struct"
                    ):
                        result_dict[field_name] = {
                            "fields": merge_schemas([result_dict[field_name], field])[
                                "fields"
                            ],
                            "name": field_name,
                            "type": "struct",
                        }
                    else:
                        # Merge the two type into a union, taking into account that one or both of them
                        # may already be unions
                        result_types = (
                            result_dict[field_name]["types"]
                            if result_dict[field_name]["type"] == "union"
                            else [result_dict[field_name]]
                        )
                        field_types = (
                            field["types"] if field["type"] == "union" else [field]
                        )
                        result_dict[field_name] = {
                            "type": "union",
                            "types": get_distinct_dictionaries(
                                remove_names(result_types) + remove_names(field_types)
                            ),
                            "name": field_name,
                        }

    return {"fields": list(result_dict.values()), "type": "struct"}


def get_distinct_dictionaries(dictionaries: list[dict]) -> list[dict]:
    """
    Get distinct dictionaries from a list of dictionaries.
    Args:
        dictionaries (list[dict]): List of dictionaries.
    Returns:
        list[dict]: List of distinct dictionaries.
    """
    # Remove duplicates, use a list instead of a set to avoid
    # errors about unhashable types
    distinct = []
    for d in dictionaries:
        if d not in distinct:
            distinct.append(d)
    # Sort for testing so we have deterministic results
    return sorted(
        distinct,
        key=lambda x: x["type"],
    )


def remove_names(list: list[dict]) -> list[dict]:
    """
    Remove names from a list of dictionaries.
    Args:
        list (dict): List of dictionaries.
    Returns:
        dict: List of dictionaries without names.
    """
    for t in list:
        if "name" in t:
            del t["name"]
    return list
