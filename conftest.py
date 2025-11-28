# conftest.py
import datetime
from pathlib import Path

import pytest

from framework.api_handler.api import APIHandler
from framework.cloud_resources.buckets.buckets import BucketInterface
from framework.config import REPORTS_DIR
from framework.logging.logger import logger
from framework.reporter.report_generator import CSVReportGenerator
from framework.utils.time_utils import time_stamp


def pytest_addoption(parser):
    parser.addoption(
        "--endpoints",  # Note: There's a typo here; it should be "--endpoints"
        action="store",
        default="http://localhost:8000",
        help="Comma-separated list of API base URLs to test against.",
    )
    parser.addoption(
        "--cloud-provider",
        action="store",
        default="azure",
        help="Choose storage provider: aws, gcp, or azure",
    )
    # add biloian flag ci
    parser.addoption(
        "--ci",
        action="store_true",
        default=False,
        help="Flag to indicate if tests are running in CI environment",
    )


def pytest_collection_modifyitems(config, items):
    """
    This hook runs after test collection.
    It checks each test item, and if "api" is in the test name,
    it adds the "api" marker to that test.
    """
    for item in items:
        if "api" in item.name.lower():
            item.add_marker(pytest.mark.api)


def pytest_generate_tests(metafunc):
    """
    This hook runs during test collection.
    It checks if a test asks for the 'dynamic_url' fixture.
    If so, it generates a test for every URL provided in the CLI option.
    """
    if "dynamic_url" in metafunc.fixturenames:
        raw_urls = metafunc.config.getoption("--endpoints")

        # Example: "http://dev, http://prod" -> ['http://dev', 'http://prod']
        url_list = [url.strip() for url in raw_urls.split(",") if url.strip()]

        metafunc.parametrize("dynamic_url", url_list, scope="session")


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report):
    """
    Hook to access the report data before it is saved to disk.
    """
    logger.info("JSON Report generated. Converting to CSV...")

    csv_path = Path(REPORTS_DIR) / "api_test_report.csv"

    generator = CSVReportGenerator(report_data=json_report, output_csv_path=csv_path)

    if generator.generate():
        logger.info(f"CSV Report successfully created at: {csv_path}")
    else:
        logger.error("Failed to create CSV report.")


def pytest_sessionfinish(session, exitstatus):
    if session.config.getoption("--ci"):
        logger.info("CI flag detected; skipping report upload.")
        return

    provider_name = session.config.getoption("--cloud-provider")
    logger.info(f"Cloud Provider selected for tests: {provider_name}")
    bucket = BucketInterface.get_bucket_class(provider_name)

    report_name = f"test_report_{provider_name}-{time_stamp()}.csv"
    bucket.upload_file(REPORTS_DIR + "/api_test_report.csv", report_name)
    logger.info(f"Uploaded report file at: {report_name}")

    logger.info(f"\nAPI session closed for {provider_name}")


@pytest.fixture(scope="session")
def api(dynamic_url):
    client = APIHandler(base_url=dynamic_url)

    if not client.ping():
        pytest.skip(f"Could not connect to API at {dynamic_url}. Skipping API tests.")

    yield client

    logger.info(f"\nAPI session closed for {dynamic_url}.")
