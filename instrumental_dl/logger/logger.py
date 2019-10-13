import logging
from datetime import datetime
from os import path, mkdir

from ..common.io import rename_all_files
from ..common.path import goto_music
from ..common.args import is_verbose


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
        self.elapsed = 0
        self.download_elapsed = 0
        self.conversion_elapsed = 0
        self.song_count = 0
        self.file_names = []
        self.song_titles = []
        self.log_mode = False

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
            if is_verbose():
                print(f'Downloaded {download["filename"]}.')

    def print_log(self, elapsed: float):
        """Prints the final log when all of the instrumentals finish"""
        self.elapsed = round(elapsed, 2)
        self.download_elapsed = round(self.download_elapsed, 2)
        self.conversion_elapsed = round(elapsed - self.download_elapsed, 2)
        rename_all_files(self, self.file_names)
        self._write_song_log()
        if is_verbose():
            # Verbose message
            print(f'Downloading {self.song_count} songs took {self.download_elapsed} '
                  f'seconds.\nConversion took {self.conversion_elapsed} ',
                  f'seconds, and full process took {self.elapsed} seconds.')
        else:
            print(f'Downloaded {self.song_count} songs in {self.elapsed} seconds.')

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

    def _write_song_log(self):
        """Writes all of the song titles and their downloaded file name to
        a log so that users can see when a wrong song is downloaded"""
        with open(f'{self._create_log_dir()}/download_list.txt', 'w+') as file:
            for i in range(len(self.file_names)):
                file.write(f'{self.song_titles[i]} as: {self.file_names[i]} \n')
