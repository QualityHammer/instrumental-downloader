from time import time
from urllib.request import urlopen
from socket import gaierror
from ssl import SSLContext

from instrumental_dl.common.errors import NoInternetConnectionError
from .youtube_dl_wrapper import YoutubeDL
from instrumental_dl.logger import Logger
from .common.arg_handler import ArgHandler


class InstrumentalDownloader:
    """The main class that handles the instrumental downloading process"""

    def __init__(self):
        """
        Attributes
        ----------
        logger: Logger
            The main logger for the process
        start_time
            The time that the process started
        youtube_dl: YoutubeDL
            The YoutubeDL object used to interact with the youtube-dl API
        """
        ArgHandler.arg_init()
        self.ssl_context = SSLContext()
        self.logger = Logger()
        self.start_time = time()
        self.youtube_dl = YoutubeDL(self.logger, self.ssl_context)

    def run(self):
        """The main method to run the process"""
        self._check_for_internet()
        # Download songs
        self.youtube_dl.download_songs(ArgHandler.get_song_names())
        # Print log
        self.logger.print_log(time() - self.start_time)

    def _check_for_internet(self):
        """Asserts that the user has a working internet connection

        Raises
        ------
        NoInternetConnectionError if the user is not connected to the internet.
        """
        try:
            _ = urlopen('https://www.google.com/', timeout=10, context=self.ssl_context)
            return True
        except gaierror:
            raise NoInternetConnectionError(self.logger)
