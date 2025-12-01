import allure
import pytest


@allure.tag("Nightly", "API")
@pytest.mark.demo
def test_get_demo_api(api):
    assert 1


@allure.tag("Nightly", "API")
@pytest.mark.demo
def test_post_demo_api(api):
    assert 1


@allure.tag("Nightly", "API")
@pytest.mark.demo
def test_put_demo_api(api):
    assert 1
