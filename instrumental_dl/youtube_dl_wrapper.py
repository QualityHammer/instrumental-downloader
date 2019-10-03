import os
import youtube_dl

from instrumental_dl.url_query import get_urls
from instrumental_dl.logger.logger import Logger


class YoutubeDL:
    """A class used as a wrapper for youtube-dl.

    Attributes:
        options -- The options used to download and convert
                   using youtube-dl.
    """

    def __init__(self, logger: Logger):
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
        self.change_output()

    @staticmethod
    def change_output():
        """Moves current directory to the output."""
        os.chdir(os.getcwd() + '/../output')

    def download_songs(self, song_names):
        """Downloads all of the instrumentals in song_names using youtube-dl."""
        urls = get_urls(song_names)
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download(urls)
