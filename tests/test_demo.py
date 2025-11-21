# create simple test file to test api handler


def test_get_status(api):
    response = api.get("/status")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"
