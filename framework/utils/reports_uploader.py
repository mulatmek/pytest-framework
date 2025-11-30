# wrapp it to a funciton that can be used in the conftest.py file
import shutil
import subprocess
import tempfile
from pathlib import Path

from framework.config import REPORTS_DIR
from framework.logging.logger import logger
from framework.utils.time_utils import time_stamp


def upload_reports(bucket, provider_name):
    logger.info(f"\nStarting API session for {provider_name}")

    results_dir = Path(REPORTS_DIR) / "allure-results"
    html_dir = Path(REPORTS_DIR) / "allure-report"

    try:
        if results_dir.exists() and any(results_dir.iterdir()):
            logger.info("Generating Allure HTML report...")
            proc = subprocess.run(
                [
                    "allure",
                    "generate",
                    str(results_dir),
                    "-o",
                    str(html_dir),
                    "--clean",
                ],
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                logger.warning(f"Allure generation failed: {proc.stderr.strip()}")
            elif html_dir.exists():
                logger.info("Zipping Allure HTML report for upload...")
                with tempfile.TemporaryDirectory() as td:
                    archive_base = Path(td) / f"allure-report-{time_stamp()}"
                    archive_path = shutil.make_archive(
                        str(archive_base), "zip", root_dir=str(html_dir)
                    )
                    upload_name = f"allure-report-{provider_name}-{time_stamp()}.zip"
                    bucket.upload_file(archive_path, upload_name)
                    logger.info(f"Uploaded Allure report as: {upload_name}")
        else:
            logger.info("No Allure results found; skipping Allure upload.")
    except Exception as exc:
        logger.exception(f"Failed to generate/upload Allure report: {exc}")

    logger.info(f"\nAPI session closed for {provider_name}")
