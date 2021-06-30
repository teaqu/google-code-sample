"""A video playlist class."""

class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name: str):
        """Playlist constructor."""
        self._name = name
        self._video_ids = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def video_ids(self) -> list:
        return self._video_ids

    def add_video(self, video_id: str):
        self._video_ids.append(video_id)

    def remove_video(self, video_id: str):
        self._video_ids.remove(video_id)

    def has_video(self, video_id: str):
        return video_id in self._video_ids

    def clear_videos(self):
        self._video_ids = []
