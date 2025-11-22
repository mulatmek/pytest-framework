# conftest.py
import pytest

from framework.api_handler.api import APIHandler
from framework.logging.logger import logger


def pytest_addoption(parser):
    parser.addoption(
        "--endpoints",  # Note: There's a typo here; it should be "--endpoints"
        action="store",
        default="http://localhost:8000",
        help="Comma-separated list of API base URLs to test against.",
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
        # 1. Get the string from command line
        raw_urls = metafunc.config.getoption("--endpoints")

        # 2. Split string into a list and clean up whitespace
        # Example: "http://dev, http://prod" -> ['http://dev', 'http://prod']
        url_list = [url.strip() for url in raw_urls.split(",") if url.strip()]

        # 3. Tell pytest to create a test case for each URL
        metafunc.parametrize("dynamic_url", url_list, scope="session")


@pytest.fixture(scope="session")
def api(dynamic_url):
    # 1. Setup Phase
    client = APIHandler(base_url=dynamic_url)

    if not client.ping():
        pytest.skip(f"Could not connect to API at {dynamic_url}. Skipping API tests.")

    yield client  # <-- Execution pauses here until all tests using 'api' are done

    logger.info(f"\nAPI session closed for {dynamic_url}.")
