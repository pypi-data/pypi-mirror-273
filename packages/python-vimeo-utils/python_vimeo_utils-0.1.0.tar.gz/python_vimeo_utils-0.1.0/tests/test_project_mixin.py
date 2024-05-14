from http import HTTPStatus

import pytest
from vimeo_utils.utils import get_project_id_from_uri


@pytest.fixture(scope="module")
def project_id(vclient):
    # Setup: Create a new project and retrieve its ID
    response = vclient.create_project("Test Project")
    assert response.status_code == HTTPStatus.CREATED

    # This is where the tests will be run
    project_id = get_project_id_from_uri(response.json()["uri"])
    yield project_id

    # Teardown: Delete the project using its ID
    response = vclient.delete_project(project_id)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_create_project(project_id):
    assert project_id is not None
    assert isinstance(project_id, str)


def test_get_project(vclient, project_id):
    response = vclient.get_project(project_id)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Test Project"


def test_edit_project(vclient, project_id):
    response = vclient.edit_project(project_id, "Test edit")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Test edit"


def test_get_all_projects(vclient):
    response = vclient.get_all_projects()
    assert response.status_code == HTTPStatus.OK
    expected_keys = {"total", "page", "per_page", "paging", "data"}
    assert all(key in response.json() for key in expected_keys)


# def test_move_to_project(vimeo_client, project_id, video_uri):
#     video_id = get_video_id_from_uri(video_uri)
#     response = move_to_project(vimeo_client, project_id, video_id)
#     assert response.status_code == HTTPStatus.NO_CONTENT


# def test_get_videos_from_folder(vimeo_client):
#     response = get_videos_from_folder(
#         vimeo_client, os.getenv("VIMEO_USER_ID"), os.getenv("VIMEO_FOLDER_ID")
#     )
#     expected_keys = {"total", "page", "per_page", "paging", "data"}
#     assert all(key in response for key in expected_keys)
