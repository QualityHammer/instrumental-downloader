import logging
import datetime

from ..common.io import rename_all_files
from ..common.path import goto_program


class Logger:
    """A custom logger class used for logging song downloads, errors, and
    youtube-dl errors and info.

    Attributes:
        elapsed -- The amount of time elapsed during the download and conversion
        download_elapsed -- The amount of time elapsed during the download
        conversion_elapsed -- The amount of time elapsed during the conversion
        song_count -- The amount of songs downloaded
        file_names -- A list of all of the file names
        song_titles -- A list of all of the song titles
        log_mode -- Set to true when an error has occurred and a log file
                    has been created
    """

    def __init__(self):
        song_titles = []
        self.elapsed = 0
        self.download_elapsed = 0
        self.conversion_elapsed = 0
        self.song_count = 0
        self.file_names = []
        self.song_titles = song_titles.copy()
        self.log_mode = False

    def add_song_titles(self, song_titles: list):
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
            self.log_append(download['filename'], download['elapsed'])

    def print_log(self, elapsed: float):
        """Prints the final log when all of the instrumentals finish"""
        self.elapsed = elapsed
        self.conversion_elapsed = elapsed - self.download_elapsed
        rename_all_files(self, self.file_names)
        self._write_song_log()
        # Verbose message
        print('Downloading', self.song_count, 'songs took', self.download_elapsed,
              'seconds.\nConversion took', self.conversion_elapsed,
              'seconds, and full process took', self.elapsed, 'seconds.')

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

    def _log_mode_on(self):
        """Configs and turns on log mode when an error/ warning has occurred"""
        goto_program()
        if not self.log_mode:
            self.log_mode = True
            logging.basicConfig(filename='log/errors/' + str(datetime.datetime.now()) +
                                         '.log', filemode='w',
                                format='%(name)s - %(levelname)s - %(message)s')

    def _write_song_log(self):
        """Writes all of the song titles and their downloaded file name to
        a log so that users can see when a wrong song is downloaded"""
        with open('log/download_list.txt', 'w+') as file:
            for i in range(len(self.file_names)):
                file.write(self.song_titles[i] + ' as: ' + self.file_names[i] + '\n')
