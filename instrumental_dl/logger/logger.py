import logging
from datetime import datetime
from os import path, mkdir

from ..common.path import goto_music
from ..common.args import ArgHandler
from ..common.const_messages import ConstMessages


class Logger:
    """A custom logger class used for logging song downloads, errors, and
    youtube-dl errors and info.

    Attributes:
        file_name -- The name of the log file used if an error occurs. Starts as None
        elapsed -- The amount of time elapsed during the download and conversion
        download_elapsed -- The amount of time elapsed during the download
        conversion_elapsed -- The amount of time elapsed during the conversion
        song_count -- The amount of songs downloaded
        file_names -- A list of all of the file names
        song_titles -- A list of all of the song titles
        failed_songs -- A list of any songs that had no instrumentals found
        log_mode -- Set to true when an error has occurred and a log file
                    has been created
    """

    def __init__(self):
        self.elapsed = 0
        self.download_elapsed = 0
        self.conversion_elapsed = 0
        self.song_count = 0
        self.file_names = []
        self.song_titles = []
        self.failed_songs = []
        self.log_mode = False

    def add_failed_songs(self, failed_songs: list):
        """Adds all songs that failed to the list of failed songs."""
        self.failed_songs = failed_songs

    def add_song_titles(self, song_titles: list):
        """Adds all of the song titles to the log."""
        self.song_titles = song_titles

    def log_append(self, filename: str, elapsed: float):
        """Adds an instrumental to the log when it's finished downloading"""
        self.song_count += 1
        self.download_elapsed += elapsed
        self.song_titles.append(filename[:-4])
        self.file_names.append(filename)

    def hook(self, download):
        """Youtube-dl hook used to add instrumentals to the log as
        they finish downloading"""
        if download['status'] == 'finished':
            try:
                self.log_append(download['filename'], download['elapsed'])
            except KeyError:
                self.log_append(download['filename'], 0)

            if ArgHandler.is_verbose():
                print(ConstMessages.verbose_song_downloaded_message(download["filename"]))

    def print_log(self, elapsed: float):
        """Prints the final log when all of the instrumentals finish"""
        self.elapsed = round(elapsed, 2)
        self.download_elapsed = round(self.download_elapsed, 2)
        self.conversion_elapsed = round(elapsed - self.download_elapsed, 2)
        self._write_song_log()
        self._print_message()

    def debug(self, msg):
        pass

    def warning(self, msg):
        """Logs a warning message"""
        self._log_mode_on()
        logging.warning(msg)

    def error(self, msg):
        """Logs an error message"""
        self._log_mode_on()
        logging.error(msg)

    @staticmethod
    def _create_log_dir():
        """Creates a directory for logs in ~/music/Instrumentals if it
        doesn't exist.

        :return: log_dir: The name of the log directory"""
        log_dir = 'instrumental_dl_log'
        if not path.exists(log_dir):
            mkdir(log_dir)
        return log_dir

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
        # Console message only displays if more than one instrumental was successfully downloaded
        print('')
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
                print(ConstMessages.no_instrumental)
                # Prints out each song that failed
                for song in self.failed_songs:
                    print(song)
            else:
                print(ConstMessages.no_instrumental_basic)

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
