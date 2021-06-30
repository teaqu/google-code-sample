"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id
        self._flag_reason = ""
        self._flagged = False

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def flagged(self) -> bool:
        """Returns the video id of a video."""
        return self._flagged

    @property
    def flag_reason(self) -> str:
        """Returns the video id of a video."""
        return self._flag_reason

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    def flag(self, flag_reason="Not supplied"):
        """Returns the video id of a video."""
        self._flagged = True
        self._flag_reason = flag_reason

    def allow(self):
        self._flagged = False
        self._flag_reason = ""

    def __str__(self):
        tags = ' '.join(self.tags)
        out = self.title + " (" + self.video_id + ") [" + tags + "]"

        if self._flagged:
            out += " - FLAGGED (reason: " + self.flag_reason + ")"

        return out
