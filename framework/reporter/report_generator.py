import csv
from pathlib import Path
from typing import Any, Dict, List


class CSVReportGenerator:
    def __init__(self, report_data: Dict[str, Any], output_csv_path: Path) -> None:
        """
        :param report_data: The dictionary object from pytest-json-report
        :param output_csv_path: Where to save the generated CSV
        """
        self.report_data = report_data
        self.output_csv_path = Path(output_csv_path)

    def _extract_message(self, test_data: Dict[str, Any]) -> str:
        """Extracts error message or skip reason."""
        stages = ["call", "setup", "teardown"]
        for stage in stages:
            if stage in test_data:
                stage_data = test_data[stage]
                if "longrepr" in stage_data:
                    return str(stage_data["longrepr"])
                if "crash" in stage_data:
                    return stage_data["crash"].get("message", "")
        return ""

    def _calculate_duration(self, test_data: Dict[str, Any]) -> float:
        """Sums up setup, call, and teardown duration."""
        total = 0.0
        for stage in ["setup", "call", "teardown"]:
            if stage in test_data:
                total += test_data[stage].get("duration", 0.0)
        return round(total, 4)

    def generate(self):
        """Generates the CSV file from the internal dictionary."""
        tests = self.report_data.get("tests", [])

        # CSV Headers
        headers = ["Test Name", "Status", "Duration (s)", "Message"]

        try:
            # Ensure directory exists
            self.output_csv_path.parent.mkdir(parents=True, exist_ok=True)

            with open(
                self.output_csv_path, "w", newline="", encoding="utf-8"
            ) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)

                for test in tests:
                    node_id = test.get("nodeid", "Unknown")
                    outcome = test.get("outcome", "Unknown").upper()
                    duration = self._calculate_duration(test)
                    message = self._extract_message(test)

                    writer.writerow([node_id, outcome, duration, message])

            return True
        except Exception as e:
            print(f"Failed to write CSV: {e}")
            return False
