from http import HTTPStatus

from vimeo_utils.client import VimeoAPIClient
from vimeo_utils.constants import TranscodeStatus
from vimeo_utils.constants import VideoStatus


def test_upload_video(video_uri):
    assert video_uri is not None
    assert isinstance(video_uri, str)


def test_get_video(vclient: VimeoAPIClient, video_uri):
    response = vclient.get_video(video_uri)
    assert response.status_code == HTTPStatus.OK
    expected_keys = [
        "uri",
        "name",
        "description",
        "link",
        "created_time",
        "privacy",
        "download",
        "status",
        "upload",
        "transcode",
        "is_playable",
    ]
    assert all(key in response.json() for key in expected_keys)


def test_edit_video(vclient, video_uri):
    params = {
        "name": "Test edit",
        "description": "Test edit",
    }
    response = vclient.edit_video(video_uri, params)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Test edit"
    assert response.json()["description"] == "Test edit"


def test_get_transcode_status(vclient, video_uri):
    response = vclient.get_transcode_status(video_uri)
    allowed_statuses = [
        TranscodeStatus.COMPLETE,
        TranscodeStatus.ERROR,
        TranscodeStatus.IN_PROGRESS,
    ]
    assert any(status in response for status in allowed_statuses)


def test_get_status(vclient, video_uri):
    response = vclient.get_status(video_uri)
    allowed_statuses = [
        VideoStatus.AVAILABLE,
        VideoStatus.TRANSCODE_STARTING,
        VideoStatus.TRANSCODING,
        VideoStatus.TRANSCODING_ERROR,
        VideoStatus.UNAVAILABLE,
        VideoStatus.UPLOADING,
        VideoStatus.UPLOADING_ERROR,
    ]
    assert any(status in response for status in allowed_statuses)


def test_is_available(vclient, video_uri):
    response = vclient.is_available(video_uri)
    assert response is True


def test_is_transcode_complete(vclient, video_uri) -> bool:
    response = vclient.is_transcode_complete(video_uri)
    assert response is True


def test_is_playable(vclient, video_uri):
    response = vclient.is_playable(video_uri)
    assert response is True


def test_get_download_link(vclient, video_uri):
    response = vclient.get_download_link(video_uri)
    assert response is not None
    assert response.startswith("https://player.vimeo.com/progressive_redirect/download")


def test_add_domain_to_whitelist(vclient, video_uri):
    domain = "example.com"
    response = vclient.add_domain_to_whitelist(video_uri, domain)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_all_videos(vclient):
    response = vclient.get_all_videos()
    assert isinstance(response, list)
    assert all(isinstance(video, dict) for video in response)
    expected_keys = {"uri", "name", "created_time", "status"}
    assert all(expected_keys.issubset(video.keys()) for video in response)
