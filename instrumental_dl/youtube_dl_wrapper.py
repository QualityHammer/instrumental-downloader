import youtube_dl
from ssl import SSLContext

from .common.io import rename_all_files
from .common.url_query import get_video_urls
from .common.path import goto_music
from .logger import Logger


class YoutubeDL:
    """A class used as a wrapper for youtube-dl."""

    def __init__(self, logger: Logger, ssl_context: SSLContext):
        """
        Parameter
        ---------
        logger: Logger
            The main logger object.

        Attribute
        ----------
        options: dict
            The options used to download and convert using youtube-dl.
        """
        self.logger = logger
        self.ssl_context = ssl_context
        self.options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': self.logger,
            'progress_hooks': [self.logger.hook],
            'nocheckcertificate': True,
            'outtmpl': '%(title)s.%(ext)s',
        }

    def download_songs(self, song_names: list):
        """Downloads all of the instrumentals in song_names using youtube-dl.

        Parameter
        ---------
        song_names: list of str
            A list of all the song names to be downloaded.
        """
        # Moves current directory to music/Instrumentals/
        goto_music()
        # Get urls to download and lists to log
        urls, failed_songs, song_names = get_video_urls(song_names, self.ssl_context)
        if len(failed_songs) > 0:
            self.logger.add_failed_songs(failed_songs)
        self.logger.add_song_titles(song_names)
        # Downloads all instrumentals
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download(urls)

        rename_all_files(self.logger)
