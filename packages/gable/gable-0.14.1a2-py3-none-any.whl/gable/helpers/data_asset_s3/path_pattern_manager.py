import re
from datetime import datetime
from typing import Dict, Iterable, Optional
from urllib.parse import unquote

from gable.helpers.data_asset_s3.logger import log_debug

YEAR_REGEX = r"20\d{2}"
MONTH_REGEX = r"0[1-9]|1[0-2]"
DAY_REGEX = r"0[1-9]|[12][0-9]|3[01]"
HOUR_REGEX = r"[01][0-9]|2[0-3]"
MINUTE_REGEX = r"[0-5][0-9]"
EPOCH_REGEX = r"(?<!\d)\d{10}(?!\d)"

DATE_PLACEHOLDER_TO_REGEX = {
    "{YYYY-MM-DD:HH:mm}": f"({YEAR_REGEX})-({MONTH_REGEX})-({DAY_REGEX}):({HOUR_REGEX}):({MINUTE_REGEX})",
    "{YYYYMMDD:HH:mm}": f"({YEAR_REGEX})({MONTH_REGEX})({DAY_REGEX}):({HOUR_REGEX}):({MINUTE_REGEX})",
    "{YYYY}/{MM}/{DD}/{HH}": f"({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})/({HOUR_REGEX})",
    "{YYYY-MM-DD:HH}": f"({YEAR_REGEX})-({MONTH_REGEX})-({DAY_REGEX}):({HOUR_REGEX})",
    "{YYYYMMDD_HH}": f"({YEAR_REGEX})({MONTH_REGEX})({DAY_REGEX})_({HOUR_REGEX})",
    "{YYYYMMDD:HH}": f"({YEAR_REGEX})({MONTH_REGEX})({DAY_REGEX}):({HOUR_REGEX})",
    "{YYYYMMDDHH}": f"({YEAR_REGEX})({MONTH_REGEX})({DAY_REGEX})({HOUR_REGEX})",
    "{YYYY}/{MM}/{DD}": f"({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})",
    "{YYYY-MM-DD}": f"({YEAR_REGEX})-({MONTH_REGEX})-({DAY_REGEX})",
    "{YYYYMMDD}": f"({YEAR_REGEX})({MONTH_REGEX})({DAY_REGEX})",
}
EPOCH_PLACEHOLDER_TO_REGEX = {
    "{epoch}": EPOCH_REGEX,
}
NUMBER_PLACEHOLDER_TO_REGEX = {
    "{N}": r"\d+",
}


class PathPatternManager:
    """
    Manages the transformation and storage of file paths based on specified patterns.
    This class provides functionalities to add file paths after transforming them
    to a standardized format and to retrieve these paths based on matching patterns.

    Attributes:
        pattern_to_paths Dict[str, re.Pattern]: A dictionary that maps transformed
        path patterns to list of regex used to search for s3 files.
        pattern_to_actual_paths Dict[str, set[str]]: A dictionary that maps
        path patterns to the actual file paths that match the pattern.
    """

    def __init__(self):
        self.pattern_to_regex_paths: Dict[str, re.Pattern] = {}
        self.pattern_to_actual_paths: Dict[str, dict[str, Optional[datetime]]] = {}

    def substitute_if_unix_timestamp(self, path: str) -> str:
        """
        Checks if the path segment contains a UNIX timestamp and
        replaces it with a placeholder.
        """
        match = re.search(EPOCH_PLACEHOLDER_TO_REGEX["{epoch}"], path)
        if match:
            timestamp = int(match.group(0))
            try:
                date_time = datetime.fromtimestamp(timestamp)
                if datetime(2000, 1, 1) <= date_time <= datetime(2030, 12, 31):
                    path = path.replace(match.group(0), "{epoch}")
            except ValueError:
                pass
        return path

    def substitute_unknown_numbers_placeholder(self, path: str) -> str:
        """
        At this point any remaining numbers in the path are likely not dates. We can replace them with a placeholder,
        which allows us to group together paths that are similar except for the numbers.

        Example:
            2024/01/01/data.part1.csv and 2024/01/01/data.part2.csv -> 2024/01/01/data.part{N}.csv
        """

        return re.sub(NUMBER_PLACEHOLDER_TO_REGEX["{N}"], "{N}", path)

    def substitute_date_placeholders(self, path) -> tuple[str, Optional[datetime]]:
        """
        Applies regex patterns to replace date placeholders in paths with their regex equivalents.

        Args:
            path (str): The file path that may contain date patterns.

        Returns:
            str: The file path with dates standardized to placeholders.
        """
        date = None
        for placeholder, regex in DATE_PLACEHOLDER_TO_REGEX.items():
            match = re.search(regex, path)
            if match:
                path = path.replace(match.group(0), placeholder)
                # If date is already set, we don't want to overwrite it since we want the most specific
                # date available (order of regex patterns matters)
                if not date and len(match.groups()) > 3:
                    # All regex patterns have year, month, day
                    date = datetime(
                        year=int(match.group(1)),
                        month=int(match.group(2)),
                        day=int(match.group(3)),
                        hour=int(match.group(4)) if len(match.groups()) > 3 else 0,
                        minute=int(match.group(5)) if len(match.groups()) > 4 else 0,
                    )
        path = self.substitute_if_unix_timestamp(path)
        path = self.substitute_unknown_numbers_placeholder(path)
        return path, date

    def template_to_regex(self, template) -> re.Pattern:
        """Converts a string template with placeholders into a regex pattern."""
        regex_pattern = template
        for placeholder, regex in DATE_PLACEHOLDER_TO_REGEX.items():
            regex_pattern = regex_pattern.replace(placeholder, regex)
        return re.compile(regex_pattern)

    def get_all_patterns(self) -> Iterable[str]:
        """
        Returns a list of all patterns that have been added to the manager.
        """
        return self.pattern_to_regex_paths.keys()

    def get_pattern_to_actual_paths(self) -> Dict[str, Dict[str, Optional[datetime]]]:
        """
        Returns a dictionary of all patterns and their corresponding file paths.
        """
        return self.pattern_to_actual_paths

    def get_regex_from_pattern(self, pattern: str) -> Optional[re.Pattern]:
        """
        Returns the matching regex for pattern that has been added to the manager.
        """
        return self.pattern_to_regex_paths.get(pattern, None)

    def add_filepaths(self, filepath: list[str]) -> int:
        """
        Transforms a file path based on predefined patterns and stores the transformed
        path along with the original file path in the manager.

        Args:
            filepath (str): The file path to be added, which will be transformed and stored.
        Returns:
            int: Number of new patterns added to the manager.
        """
        unique_filepaths = set(filepath)
        new_patterns = 0

        for path in unique_filepaths:
            unquoted_path = path
            try:
                while unquoted_path != (unquoted_path := unquote(unquoted_path)):
                    pass
                transformed_path, dt = self.substitute_date_placeholders(unquoted_path)
                if transformed_path not in self.pattern_to_regex_paths:
                    regex_pattern = self.template_to_regex(transformed_path)
                    self.pattern_to_regex_paths[transformed_path] = regex_pattern
                    self.pattern_to_actual_paths[transformed_path] = {}
                    new_patterns += 1
                # TODO: Logic to keep the most recent N entries for each pattern
                self.pattern_to_actual_paths[transformed_path][path] = dt
            except Exception as e:
                log_debug(f"Error adding file paths '{unquoted_path}': {e}")
        return new_patterns
