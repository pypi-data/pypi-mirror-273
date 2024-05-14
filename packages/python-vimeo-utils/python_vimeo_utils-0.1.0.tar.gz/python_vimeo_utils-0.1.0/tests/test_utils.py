from vimeo_utils.utils import build_user_uri
from vimeo_utils.utils import extract_page_number
from vimeo_utils.utils import get_video_id_from_uri


def test_build_user_uri():
    assert build_user_uri(1234567890) == "/users/1234567890"
    assert build_user_uri(None) == "/me"


def test_extract_page_number():
    assert extract_page_number("/videos?page=2") == 2  # noqa: PLR2004
    assert extract_page_number("/videos?page=3") == 3  # noqa: PLR2004
    assert extract_page_number("/videos?page=4") == 4  # noqa: PLR2004


def test_get_video_id_from_uri():
    assert get_video_id_from_uri("/videos/1234567890") == "1234567890"
