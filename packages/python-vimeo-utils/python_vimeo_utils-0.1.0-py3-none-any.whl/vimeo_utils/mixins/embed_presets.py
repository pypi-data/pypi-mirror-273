from typing import Optional

from requests import Response


class EmbedPresetMixin:
    """
    Implementation of a subset of common methods from:
    https://developer.vimeo.com/api/reference/embed-presets#edit_embed_preset

    - Create embed preset (TODO: Not implemented yet)
    - Get embed preset (TODO: Not implemented yet)
    - Edit embed preset
    - Delete embed preset (TODO: Not implemented yet)
    """

    # --------------------------------------------------------------------------
    # Essentials
    # --------------------------------------------------------------------------

    def edit_embed_preset(self, vimeo_uri: str, preset_id: int) -> Response:
        """Edit the embed preset."""
        uri = f"{vimeo_uri}/presets/{preset_id}"
        response = self.client.put(uri)
        response.raise_for_status()
        return response
