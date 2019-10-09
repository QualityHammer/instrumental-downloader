import os
import youtube_dl

from .url_query import get_urls
from .logger.logger import Logger
from .common.path import goto_program, goto_music


class YoutubeDL:
    """A class used as a wrapper for youtube-dl.

    Attributes:
        options -- The options used to download and convert
                   using youtube-dl.
    """

    def __init__(self, logger):
        self.options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': Logger(),
            'progress_hooks': [logger.hook],
            'nocheckcertificate': True,
            'outtmpl': '%(title)s.%(ext)s',
        }

    def download_songs(self, song_names):
        """Downloads all of the instrumentals in song_names using youtube-dl."""
        goto_music()
        urls = get_urls(song_names)
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download(urls)
