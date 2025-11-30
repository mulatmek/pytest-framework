# wrapp it to a funciton that can be used in the conftest.py file
import shutil
import subprocess
import tempfile
from pathlib import Path

from framework.config import REPORTS_DIR, RESULTS_DIR, HTMl_DIR
from framework.logging.logger import logger
from framework.utils.time_utils import time_stamp


def generate_allure_reports():
    """
    generate Allure reports
    :return:
    """
    proc = subprocess.run(
        [
            "allure",
            "generate",
            str(RESULTS_DIR),
            "-o",
            str(HTMl_DIR),
            "--clean",
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        logger.warning(f"Allure generation failed: {proc.stderr.strip()}")
        return False
    return True


def upload_allure_report(bucket, provider_name):
    """
    upload Allure report to cloud provider
    :param bucket:
    :param provider_name:
    :return:
    """
    logger.info(f"\nStarting API session for {provider_name}")
    try:
        if RESULTS_DIR.exists() and any(RESULTS_DIR.iterdir()):
            if HTMl_DIR.exists():
                logger.info("Zipping Allure HTML report for upload...")
                with tempfile.TemporaryDirectory() as td:
                    archive_base = Path(td) / f"allure-report-{time_stamp()}"
                    archive_path = shutil.make_archive(
                        str(archive_base), "zip", root_dir=str(HTMl_DIR)
                    )
                    upload_name = f"allure-report-{provider_name}-{time_stamp()}.zip"
                    bucket.upload_file(archive_path, upload_name)
                    logger.info(f"Uploaded Allure report as: {upload_name}")
        else:
            logger.info("No Allure results found; skipping Allure upload.")
    except Exception as exc:
        logger.exception(f"Failed to generate/upload Allure report: {exc}")

    logger.info(f"\nAPI session closed for {provider_name}")
