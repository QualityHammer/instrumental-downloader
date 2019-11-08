from time import time
from urllib.request import urlopen
from socket import gaierror

from .errors import NoInternetConnectionError
from .youtube_dl_wrapper import YoutubeDL
from .logger.logger import Logger
from .common.args import arg_init, get_song_names


class InstrumentalDownloader:

    def __init__(self):
        arg_init()
        self.logger = Logger()
        self.start_time = time()
        self.youtube_dl = YoutubeDL(self.logger)

    def run(self):
        self._check_for_internet()
        # Download songs
        self.youtube_dl.download_songs(get_song_names())
        # Print log
        self.logger.print_log(time() - self.start_time)

    def _check_for_internet(self):
        """Asserts that the user has a working internet connection"""
        try:
            _ = urlopen('https://www.google.com/', timeout=10)
            return True
        except gaierror:
            raise NoInternetConnectionError(self.logger)
