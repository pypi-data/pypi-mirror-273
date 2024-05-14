import os
from http import HTTPStatus

from vimeo_utils.client import VimeoAPIClient


def test_edit_embed_preset(vclient: VimeoAPIClient, video_uri_no_wait):
    preset_id = os.getenv("VIMEO_EMBED_PRESET")
    response = vclient.edit_embed_preset(video_uri_no_wait, preset_id)
    assert response.status_code == HTTPStatus.NO_CONTENT
