"""A video player class."""
import random

from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video_id = None
        self._playlists = {}
        self.playing = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = self._video_library.get_all_videos()
        for video in sorted(videos, key=lambda v: v.title):
            print("   ", video)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)

        if not video:
            print("Cannot play video: Video does not exist")
            return
        if video.flagged:
            print("Cannot play video: Video is currently flagged",
                  self._flag_reason(video.flag_reason))
            return

        if self._current_video_id:
            self.stop_video()
        self._current_video_id = video.video_id
        self.playing = True
        print("Playing video:", video.title)

    def stop_video(self):
        """Stops the current video."""
        if self._current_video_id:
            current_video = self._get_current_video()
            print("Stopping video:", current_video.title)
            self._current_video_id = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        videos = self._filter_flagged()
        if videos:
            random_video = random.choice(videos)
            self.play_video(random_video.video_id)
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        current_video = self._get_current_video()
        if current_video:
            if not self.playing:
                print("Video already paused:", current_video.title)
            else:
                self.playing = False
                print("Pausing video:", current_video.title)
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        if self._current_video_id:
            if self.playing:
                print("Cannot continue video: Video is not paused")
            else:
                current_video = self._get_current_video()
                self.playing = True
                print("Continuing video:", current_video.title)
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self._current_video_id:
            out = "Currently playing: " + str(self._get_current_video())
            if not self.playing:
                out += ' - PAUSED'
            print(out)
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        key = playlist_name.lower()
        if not self._playlists.get(key):
            self._playlists[key] = Playlist(playlist_name)
            print("Successfully created new playlist:", playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name "
                  "already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist = self._playlists.get(playlist_name.lower())
        video = self._video_library.get_video(video_id)
        if not playlist:
            print("Cannot add video to", playlist_name +
                  ": Playlist does not exist")
            return
        if not video:
            print("Cannot add video to", playlist_name +
                  ": Video does not exist")
            return
        if playlist.has_video(video_id):
            print("Cannot add video to", playlist_name +
                  ": Video already added")
            return
        if video.flagged:
            print("Cannot add video to", playlist_name +
                  ": Video is currently flagged",
                  self._flag_reason(video.flag_reason))
            return
        playlist.add_video(video_id)
        print("Added video to", playlist_name + ":", video.title)

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlists):
            print("Showing all playlists:")
            for key in sorted(self._playlists):
                print("   ", self._playlists[key].name)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlists.get(playlist_name.lower())
        if playlist:
            print("Showing playlist:", playlist_name)
            for video_id in playlist.video_ids:
                print("   ", self._video_library.get_video(video_id))
            if not playlist.video_ids:
                print("    No videos here yet")
        else:
            print("Cannot show playlist", playlist_name +
                  ": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self._playlists.get(playlist_name.lower())
        video = self._video_library.get_video(video_id)
        if not playlist:
            print("Cannot remove video from", playlist_name +
                  ": Playlist does not exist")
            return
        if not video:
            print("Cannot remove video from", playlist_name +
                  ": Video does not exist")
            return
        if not playlist.has_video(video_id):
            print("Cannot remove video from", playlist_name +
                  ": Video is not in playlist")
            return

        playlist.remove_video(video_id)
        print("Removed video from", playlist_name +
              ":", video.title)

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlists.get(playlist_name.lower())
        if playlist:
            playlist.clear_videos()
            print("Successfully removed all videos from", playlist_name)
        else:
            print("Cannot clear playlist", playlist_name +
                  ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlists.get(playlist_name.lower())
        if playlist:
            self._playlists.pop(playlist_name.lower())
            print("Deleted playlist:", playlist_name)
        else:
            print("Cannot delete playlist", playlist_name +
                  ": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        results = []
        for video in self._filter_flagged():
            if search_term.lower() in video.title.lower():
                results.append(video)

        self._select_video(results, search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        results = []
        for video in self._filter_flagged():
            if video_tag in video.tags:
                results.append(video)

        self._select_video(results, video_tag)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if not video:
            print("Cannot flag video: Video does not exist")
            return

        if video.flagged:
            print("Cannot flag video: Video is already flagged")
            return

        if self._current_video_id == video_id:
            self.stop_video()

        video.flag(flag_reason)
        print("Successfully flagged video:", video.title,
              self._flag_reason(flag_reason))

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if not video:
            print("Cannot remove flag from video: Video does not exist")
            return

        if not video.flagged:
            print("Cannot remove flag from video: Video is not flagged")
            return

        video.allow()
        print("Successfully removed flag from video:", video.title)

    def _flag_reason(self, flag_reason):
        return "(reason: " + flag_reason + ")"

    def _filter_flagged(self):
        videos = self._video_library.get_all_videos()
        return list(filter(lambda v: not v.flagged, videos))

    def _get_current_video(self):
        return self._video_library.get_video(self._current_video_id)

    def _select_video(self, results, search_term):
        if len(results):
            print("Here are the results for", search_term + ":")
            for x in range(len(results)):
                print(str(x + 1) + ")", results[x])
            print("Would you like to play any of the above? If yes, specify "
                  "the number of the video.")
            print("If your answer is not a valid number, we will assume it's "
                  "a no.")
            choice = input()
            if choice.isdigit() and 0 < int(choice) <= len(results):
                self.play_video(results[int(choice) - 1].video_id)
        else:
            print("No search results for", search_term)
