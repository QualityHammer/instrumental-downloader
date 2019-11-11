import logging
from datetime import datetime
from os import path, mkdir

from ..common.path import goto_music
from ..common.arg_handler import ArgHandler
from ..common.const_messages import ConstMessages


class Logger:
    """A custom logger class used for logging song downloads, errors, and
    youtube-dl errors and info.

    There should only be one instance of a Logger object that persists along with the script. Once a logger is created,
    the logger_available switch is turned to False.

    Attributes
    ----------
    logger_available : bool
        The switch that allows only one Logger to be created.

    Methods
    -------
    add_failed_songs(failed_songs: list of str)
        Adds all songs that failed downloading to the list of failed songs.
    add_song_titles(song_titles: list of str)
        Adds a list of song titles to the log.
    hook(download: dict)
        Youtube-dl hook that is used to add instrumentals to the log after they finish downloading.
    print_log(elapsed: float)
        Prints the final log when all of the instrumentals finish downloading and converting.
    """
    logger_available = True

    def __init__(self):
        """
        Attributes
        ----------
        file_names: list of str
            The name of the log file used if an error occurs. Starts as None
        elapsed: float
            The amount of time elapsed during the download and conversion
        download_elapsed: float
            The amount of time elapsed during the download
        conversion_elapsed: float
            The amount of time elapsed during the conversion
        song_count: int
            The amount of songs downloaded
        file_names: list of str
            A list of all of the file names
        song_titles: list of str
            A list of all of the song titles
        failed_songs: list of str
            A list of any songs that had no instrumentals found
        log_mode: bool
            Set to true when an error has occurred and a log file
                    has been created
        """
        if Logger.logger_available:
            Logger.logger_available = False
            # TODO: Add error for too many loggers
        self.elapsed = 0
        self.download_elapsed = 0
        self.conversion_elapsed = 0
        self.song_count = 0
        self.file_names = []
        self.song_titles = []
        self.failed_songs = []
        self.log_mode = False

    def add_failed_songs(self, failed_songs: list):
        """Adds all songs that failed downloading to the list of failed songs.

        Parameters
        ----------
        failed_songs: list
            A list of song titles that failed downloading for any reason.
        """
        self.failed_songs = failed_songs

    def add_song_titles(self, song_titles: list):
        """Adds a list of song titles to the log.

        Parameters
        ----------
        song_titles: list
            A list of song titles that are added to the log before they download.
        """
        self.song_titles = song_titles

    def hook(self, download: dict):
        """Youtube-dl hook that is used to add instrumentals to the log after they finish downloading.

        Parameters
        ----------
        download: dict
            The download info that has been passed from Youtube-dl on download completion
        """
        if download['status'] == 'finished':
            try:
                self._log_append(download['filename'], download['elapsed'])
            except KeyError:
                self._log_append(download['filename'], 0)

            # Verbose song download message
            if ArgHandler.is_verbose():
                print(ConstMessages.verbose_song_downloaded_message(download["filename"]))

    def print_log(self, elapsed: float):
        """Prints the final log when all of the instrumentals finish downloading and converting.

        Parameters
        ----------
        elapsed: float
            The amount of time that has elapsed throughout the whole process
        """
        self.elapsed = round(elapsed, 2)
        self.download_elapsed = round(self.download_elapsed, 2)
        self.conversion_elapsed = round(elapsed - self.download_elapsed, 2)
        self._write_song_log()
        self._print_message()

    def debug(self, msg: str):
        """Empty debug method"""
        pass

    def warning(self, msg: str):
        """Logs a warning message.
        Creates a log if needed

        Parameters
        ----------
        msg: str
            The warning message to log
        """
        self._log_mode_on()
        logging.warning(msg)

    def error(self, msg):
        """Logs an error message.
        Creates a log if needed

        Parameters
        ----------
        msg: str
            The warning message to log
            """
        self._log_mode_on()
        logging.error(msg)

    @staticmethod
    def _create_log_dir() -> str:
        """Creates a directory for logs in ~/music/Instrumentals called 'instrumental_dl_log' if it
        doesn't exist.

        Returns
        -------
        log_dir: str
            The name of the log directory
        """
        log_dir = 'instrumental_dl_log'
        if not path.exists(log_dir):
            mkdir(log_dir)
        return log_dir

    def _log_append(self, filename: str, elapsed: float):
        """Adds an instrumental's filename to the log when it's finished downloading.

        Also adds the elapsed time of that download to the total.

        Parameters
        ----------
        filename: str
            The name of the file that has been downloaded
        elapsed: float
            The amount of time that elapsed during this file's download
        """
        self.song_count += 1
        self.download_elapsed += elapsed
        self.song_titles.append(filename[:-4])
        self.file_names.append(filename)

    def _log_mode_on(self):
        """Configs and turns on log mode when an error/ warning has occurred"""
        if not self.log_mode:
            goto_music()
            self.log_mode = True
            timestamp = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S_%f')
            filename = f'{self._create_log_dir()}/log{timestamp}.log'
            logging_format = '%(name)s - %(levelname)s - %(message)s'
            logging.basicConfig(filename=filename, filemode='w', format=logging_format)

    def _print_message(self):
        """Prints either a verbose message, or short message to the console on completion"""
        print('')
        # Console message only displays if more than one instrumental was successfully downloaded
        if self.song_count != 0:
            if ArgHandler.is_verbose():
                # Verbose message
                print(ConstMessages.verbose_finished_message(self.song_count, str(self.conversion_elapsed),
                                                             str(self.download_elapsed), str(self.elapsed)))
            else:
                print(ConstMessages.finished_message(self.song_count, str(self.elapsed)))
        # Failed instrumental message
        if len(self.failed_songs) > 0:
            if ArgHandler.is_verbose():
                # Verbose message
                print(ConstMessages.no_instrumental_message_verbose)
                # Prints out each song that failed
                for song in self.failed_songs:
                    print(song)
            else:
                print(ConstMessages.no_instrumental_message)

    def _write_song_log(self):
        """Writes all of the song titles and their downloaded file name to
        a log so that users can see when a wrong song is downloaded"""
        with open(f'{self._create_log_dir()}/download_list.txt', 'w+') as file:
            # Each instrumental downloaded
            for i in range(len(self.file_names)):
                file.write(ConstMessages.log_song_download(self.song_titles[i], self.file_names[i]))
            # Any instrumentals that couldn't be found
            if len(self.failed_songs) > 0:
                file.write(ConstMessages.long_file_separator)
                for song in self.failed_songs:
                    file.write(ConstMessages.log_failed_song_download(song))
