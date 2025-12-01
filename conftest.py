# conftest.py
import pytest

from framework.api_handler.api import APIHandler
from framework.cloud_resources.buckets.buckets import BucketInterface
from framework.logging.logger import logger
from framework.report_manager.reports import (
    generate_allure_reports,
    upload_allure_report,
)


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


def pytest_sessionfinish(session, exitstatus):
    """Hook to run after all tests have completed."""

    logger.info("Generating allure report")
    report_generated = generate_allure_reports()

    if not report_generated:
        logger.warning("Allure report generation failed; skipping upload.")
        return

    if session.config.getoption("--ci"):
        logger.info("CI flag detected; skipping report upload.")
        return

    # Determine cloud provider and get corresponding bucket class
    provider_name = session.config.getoption("--cloud-provider")
    logger.info(f"Cloud Provider selected for tests: {provider_name}")
    bucket = BucketInterface.get_bucket_class(provider_name)

    upload_allure_report(bucket, provider_name)

    logger.info(f"\nReport upload session closed for {provider_name}")


@pytest.fixture(scope="session")
def api(dynamic_url):
    client = APIHandler(base_url=dynamic_url)

    if not client.ping():
        pytest.skip(f"Could not connect to API at {dynamic_url}. Skipping API tests.")

    yield client

    logger.info(f"\nAPI session closed for {dynamic_url}.")
