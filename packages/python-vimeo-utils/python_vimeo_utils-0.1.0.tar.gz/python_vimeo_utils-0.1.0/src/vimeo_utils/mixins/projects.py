from typing import Optional

from requests import Response


class ProjectMixin:
    """
    Implementation of a subset of common methods from:
    https://developer.vimeo.com/api/reference/folders

    - Create a new project
    - Get a project
    - Edit a project
    - Delete a project
    - Get all projects

    - Move a video to a project
    """

    # --------------------------------------------------------------------------
    # Essentials
    # --------------------------------------------------------------------------

    def create_project(
        self, name: str, parent_folder_uri=None, fields=None
    ) -> Response:
        """Create a new project."""
        data = {"name": name, "parent_folder_uri": parent_folder_uri}
        fields = fields or ["uri", "name"]
        params = {"fields": ",".join(fields)} if fields else {}
        response = self.client.post(
            f"{self.base_uri}/projects", data=data, params=params
        )
        response.raise_for_status()
        return response

    def get_project(
        self, project_id: int, fields: Optional[list[str]] = None
    ) -> Response:  # noqa: UP007
        """Return a project with sane defaults."""
        fields = fields or ["uri", "name"]
        params = {"fields": ",".join(fields)} if fields else {}
        response = self.client.get(
            f"{self.base_uri}/projects/{project_id}", params=params
        )
        response.raise_for_status()
        return response

    def edit_project(self, project_id: int, name: str) -> Response:
        """Edit a project."""
        data = {"name": name}
        response = self.client.patch(
            f"{self.base_uri}/projects/{project_id}", data=data
        )
        response.raise_for_status()
        return response

    def delete_project(
        self, project_id: int, should_delete_clips: bool = False
    ) -> Response:
        """Delete a project."""
        params = {"should_delete_clips": should_delete_clips}
        response = self.client.delete(
            f"{self.base_uri}/projects/{project_id}", params=params
        )
        response.raise_for_status()
        return response

    def get_all_projects(self, params: Optional[dict] = None) -> Response:  # noqa: UP007
        """Returns paginated folders belonging to the authenticated user."""
        params = params or {}
        response = self.client.get(f"{self.base_uri}/projects", params=params)
        response.raise_for_status()
        return response

    # --------------------------------------------------------------------------
    # Videos
    # --------------------------------------------------------------------------

    def move_to_project(self, project_id: int, video_uri: str) -> Response:
        """Move a video to a project."""
        response = self.client.put(f"{self.base_uri}/projects/{project_id}{video_uri}")
        response.raise_for_status()
        return response

    def get_videos_from_project(self, project_id: int) -> list[dict]:
        return self.client.get(f"{self.base_uri}/folders/{project_id}/videos")
