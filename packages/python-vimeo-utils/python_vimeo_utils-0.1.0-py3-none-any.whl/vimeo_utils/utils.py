import re


def build_user_uri(user_id: None) -> str:
    """Build the user URI."""
    if user_id:
        return f"/users/{user_id}"
    return "/me"


def get_project_id_from_uri(uri: str) -> str:
    """Get project ID from URI."""
    return uri.split("/")[-1]


def get_video_id_from_uri(uri: str) -> str:
    """Get video ID from URI."""
    return uri.split("/")[-1]


def extract_page_number(url: str) -> int:
    """Function to extract page number from a given URL."""
    match = re.search(r"page=(\d+)", url)
    return int(match.group(1)) if match else 1
