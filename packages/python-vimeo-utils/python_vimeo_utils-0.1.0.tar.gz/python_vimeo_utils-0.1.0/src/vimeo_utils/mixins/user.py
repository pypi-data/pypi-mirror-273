from typing import Optional

from requests import Response


class UserMixin:
    """
    Implementation of a subset of common methods from:
    https://developer.vimeo.com/api/reference/users

    - Get user
    - Edit user
    """

    # --------------------------------------------------------------------------
    # Essentials
    # --------------------------------------------------------------------------

    def get_user(self, fields: Optional[list[str]] = None) -> Response:  # noqa: UP007
        """Get user info with sane field defaults."""
        fields = fields or [
            "uri",
            "name",
            "link",
            "location",
            "bio",
            "short_bio",
            "created_time",
        ]
        params = {"fields": ",".join(fields)} if fields else {}

        response = self.client.get(f"{self.base_uri}", params=params)
        response.raise_for_status()
        return response

    def edit_user(self, data: Optional[dict]) -> Response:  # noqa: UP007
        """Edit user."""
        response = self.client.patch(f"{self.base_uri}", data=data)
        response.raise_for_status()
        return response
