import concurrent.futures
import time
from typing import Optional

from requests import Response

from vimeo_utils.constants import TranscodeStatus
from vimeo_utils.constants import VideoStatus
from vimeo_utils.exceptions import TranscodingError
from vimeo_utils.utils import extract_page_number


class VideoMixin:
    """
    Implementation of a subset of common methods from:
    https://developer.vimeo.com/api/reference/videos

    - Upload a video
    - Get a video
    - Edit a video
    - Delete a video

    - Add domain to whitelist
    """

    # --------------------------------------------------------------------------
    # Essentials
    # --------------------------------------------------------------------------

    def upload_video(self, video_file: str, params: dict) -> str:
        """Upload a video."""
        return self.client.upload(video_file, data=params)

    def get_video(self, vimeo_uri: str, fields: Optional[list[str]] = None) -> Response:  # noqa: UP007
        """Return a video info with sane defaults."""
        fields = fields or [
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
        params = {"fields": ",".join(fields)} if fields else {}
        response = self.client.get(vimeo_uri, params=params)
        response.raise_for_status()
        return response

    def edit_video(self, vimeo_uri: str, params: dict) -> Response:
        """Edit a video."""
        response = self.client.patch(vimeo_uri, data=params)
        response.raise_for_status()
        return response

    def delete_video(self, vimeo_uri: str) -> Response:
        """Delete a video."""
        response = self.client.delete(vimeo_uri)
        response.raise_for_status()
        return response

    def get_videos(self, page: int = 1) -> Response:
        """Get single page of videos, 100 max."""
        params = {
            "fields": "uri,name,created_time,status",
            "page": page,
            "per_page": 100,
        }
        response = self.client.get(f"{self.base_uri}/videos", params=params, timeout=60)
        response.raise_for_status()
        return response

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def get_all_videos(self) -> list[dict]:
        """Get all videos."""
        videos = []

        response = self.get_videos()
        videos.extend(x for x in response.json()["data"])

        # Extracting next and last page numbers
        paging = response.json().get("paging", {})
        next_url = paging.get("next") or ""
        last_url = paging.get("last") or ""
        next_page = extract_page_number(next_url)
        last_page = extract_page_number(last_url) or next_page
        if last_page > 1:
            last_page += 1

            # Get all the rest of the pages
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                future_to_page = {
                    executor.submit(self.get_videos, page): page
                    for page in range(next_page, last_page)
                }
                for future in concurrent.futures.as_completed(future_to_page):
                    response = future.result()
                    videos.extend(x for x in response.json()["data"])
        return videos

    def get_download_link(self, vimeo_uri: str) -> Optional[str]:  # noqa: UP007
        """Get download link. HD is priority."""
        video_info = self.get_video(vimeo_uri, fields=["download"]).json()
        if "download" in video_info:
            hd_downloads = (
                video for video in video_info["download"] if video["quality"] == "hd"
            )
            sd_downloads = (
                video for video in video_info["download"] if video["quality"] == "sd"
            )

            # Prefer HD downloads
            try:
                return max(hd_downloads, key=lambda x: x.get("height", 0))["link"]
            except ValueError:
                pass

            # If no HD downloads, get the highest quality SD download
            try:
                return max(sd_downloads, key=lambda x: x.get("height", 0))["link"]
            except ValueError:
                pass

        return None

    def get_status(self, vimeo_uri: str) -> str:
        """Get video status."""
        video_info = self.get_video(vimeo_uri, fields=["status"]).json()
        return video_info["status"]

    def get_transcode_status(self, vimeo_uri: str) -> str:
        """Get video transcode status."""
        video_info = self.get_video(vimeo_uri, fields=["transcode"]).json()
        return video_info["transcode"]["status"]

    def is_available(self, vimeo_uri) -> bool:
        return self.get_status(vimeo_uri) == VideoStatus.AVAILABLE

    def is_transcode_complete(self, vimeo_uri: str) -> bool:
        return self.get_transcode_status(vimeo_uri) == TranscodeStatus.COMPLETE

    def is_playable(self, vimeo_uri: str) -> bool:
        video_info = self.get_video(vimeo_uri, fields=["is_playable"]).json()
        return video_info["is_playable"]

    def block_until_available(self, vimeo_uri: str, interval: int = 30) -> None:
        """Blocks until video is available. Be careful with this."""
        error_statuses = {
            VideoStatus.TRANSCODING_ERROR,
            VideoStatus.UPLOADING_ERROR,
        }
        while True:
            status = self.get_status(vimeo_uri)
            if status == VideoStatus.AVAILABLE:
                return
            if status in error_statuses:
                msg = "Transcoding/Uploading error"
                raise TranscodingError(msg)
            time.sleep(interval)

    # --------------------------------------------------------------------------
    # Embed privacy
    # --------------------------------------------------------------------------

    def add_domain_to_whitelist(self, vimeo_uri: str, domain: str) -> Response:
        """Add domain to whitelist."""
        uri = f"{vimeo_uri}/privacy/domains/{domain}"
        response = self.client.put(uri)
        response.raise_for_status()
        return response
