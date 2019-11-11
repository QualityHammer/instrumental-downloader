class ConstMessages:
    """
    ConstMessages fields and methods are used to separate the display messages from the logic.

    Attributes
    ----------
    long_file_separator: str
        A separator used in the log to separate failed songs
    no_instrumental_message_verbose: str
        A verbose message explaining that instrumentals couldn't be found for some songs.
    no_instrumental_message: str
        A message explaining that instrumentals couldn't be found for some songs and what to do.
    no_instrumental_help_message: str
        A message explaining what to do if your instrumentals failed to download

    Methods
    -------
    finished_message(song_count: int, elapsed: str) -> str
        Returns the normal message that is printed on completion of all downloads, conversions, and renaming.

    """

    long_file_separator = '---------------------------------------------------\n'
    no_instrumental_message_verbose = "Instrumentals for these songs could not be found"
    no_instrumental_message = "Instrumentals for some of the songs on the list could not be found.\n"
    no_instrumental_help_message = "See download_list.txt in ~user/music/Instrumentals/instrumental_dl_log"

    @staticmethod
    def finished_message(song_count: int, elapsed: str) -> str:
        """
        Returns the normal message that is printed on completion of all downloads, conversions, and renaming.

        Parameters
        ----------
        song_count: int
            The amount of songs that finished downloading
        elapsed: str
            The full time that elapsed during the process

        Returns
        -------
        str
            The final non-verbose message
        """
        s = ConstMessages._get_s_char(song_count)
        return f'Downloaded {song_count} song{s} in {elapsed} seconds.'

    @staticmethod
    def log_song_download(song_name: str, filename: str):
        """A line in the log that describes what a song was downloaded as.

        Parameters
        ----------
        song_name: str
            The song name that was downloaded
        filename: str
            The filename of the song that was downloaded

        Returns
        -------
        str
            A line for the log that describes a song download
        """
        return f'{song_name} as: {filename} \n'

    @staticmethod
    def log_failed_song_download(song: str):
        """A String that explains that an instrumental couldn't be found.

        Parameter
        ---------
        song: str
            The song that failed to download

        Returns
        -------
        str
            A message explaining that an instrumental couldn't be found.
        """
        return f"{song}'s instrumental could not be found"

    @staticmethod
    def verbose_finished_message(song_count: int, download_elapsed: str, conversion_elapsed: str, elapsed: str):
        """Returns the verbose message that is printed on completion of all downloads, conversions, and renaming.

        Parameters
        ----------
        song_count: int
            The amount of songs that finished
        download_elapsed: str
            The time that elapsed during the download process
        conversion_elapsed: str
            The time that elapsed during the conversion and renaming process
        elapsed: str
            The full time that elapsed during the process

        Returns
        -------
        str
            The final verbose message
        """
        s = ConstMessages._get_s_char(song_count)
        return f'Downloading {song_count} song{s} took {download_elapsed} ' \
               f'seconds.\nConversion took {conversion_elapsed} ' \
               f'seconds, and full process took {elapsed} seconds.'

    @staticmethod
    def verbose_song_downloaded_message(filename: str):
        return f'Downloaded {filename}.'

    @staticmethod
    def _get_s_char(song_count: int):
        """Return's an 's' for pluralization if the amount of songs downloaded is greater than 1

        Parameter
        ---------
        song_count: int
            The amount of songs that finished

        Returns
        -------
        str
            Either a blank character '' or 's'
        """
        if song_count == 1:
            return ''
        return 's'
