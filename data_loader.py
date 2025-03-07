import os
import re
import json
from collections import defaultdict


class DataLoader:
    """Class to load report data from directory structure."""

    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.dates = self.get_sorted_dates()

    def get_sorted_dates(self):
        """Fetch and sort date directories in the given path, raise exception on invalid formats."""
        date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
        dates = []
        for entry in os.listdir(self.directory_path):
            if os.path.isdir(os.path.join(self.directory_path, entry)):
                if date_pattern.fullmatch(entry):
                    dates.append(entry)
                else:
                    raise ValueError(
                        f"Invalid directory name format: {entry}. Expected format: YYYY-MM-DD."
                    )
        return sorted(dates, reverse=True)  # Sort in descending order

    def load_data(self):
        """Load JSON data and return dictionary of each date's data."""
        report_data = defaultdict(dict)
        for date in self.dates:
            files = {
                "news": f"{self.directory_path}/{date}/news.json",
                "analysis": f"{self.directory_path}/{date}/analysis.json",
            }
            for key, file_path in files.items():
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                report_data[date][key] = data
        return report_data
