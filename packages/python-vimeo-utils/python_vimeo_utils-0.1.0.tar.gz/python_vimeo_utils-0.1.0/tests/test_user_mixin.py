from http import HTTPStatus


def test_get_user(vclient):
    response = vclient.get_user()
    assert response.status_code == HTTPStatus.OK
    expected_keys = [
        "uri",
        "name",
        "link",
        "location",
        "bio",
        "short_bio",
        "created_time",
    ]
    assert all(key in response.json() for key in expected_keys)


def test_edit_user(vclient):
    params = {"gender": "o"}
    response = vclient.edit_user(params)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["gender"] == "o"
