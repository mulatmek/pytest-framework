# conftest.py
import pytest

from framework.api_handler.api import APIHandler


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="http://localhost:8000",
        help="Base URL for the API under test (default: http://localhost:8000)",
    )


@pytest.fixture(scope="session")
def api_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture(scope="session")
def api(api_url):
    return APIHandler(base_url=api_url)
