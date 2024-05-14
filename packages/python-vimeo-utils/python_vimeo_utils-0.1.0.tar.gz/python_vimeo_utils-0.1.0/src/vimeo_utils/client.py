from typing import Optional

import vimeo

from .mixins.embed_presets import EmbedPresetMixin
from .mixins.projects import ProjectMixin
from .mixins.user import UserMixin
from .mixins.videos import VideoMixin
from .utils import build_user_uri


class VimeoAPIClient(UserMixin, VideoMixin, ProjectMixin, EmbedPresetMixin):
    """A wrapper around the Vimeo client."""

    def __init__(self, client: vimeo.VimeoClient, user_id: Optional[int] = None):  # noqa: UP007
        self.client = client
        self.user_id = user_id
        self.base_uri = build_user_uri(user_id)
