class ConstMessages:
    """
    ConstMessages fields and methods are used to separate the display messages from the logic.
    """

    long_file_separator = '---------------------------------------------------\n'
    no_instrumental = "Instrumentals for these songs could not be found:"
    no_instrumental_basic = "Instrumentals for some of the songs on the list could " \
                            "not be found.\nSee download_list.txt in " \
                            "~user/music/Instrumentals/instrumental_dl_log"

    @staticmethod
    def finished_message(song_count: int, elapsed: str):
        """
        Returns the normal message that is printed on completion of all downloads, conversions, and renaming.

        :param song_count: The amount of songs that finished
        :param elapsed: The full time that elapsed during the process
        :return: The final normal message
        """
        s = ConstMessages._get_s_char(song_count)
        return f'Downloaded {song_count} song{s} in {elapsed} seconds.'

    @staticmethod
    def log_song_download(song_name: str, filename: str):
        return f'{song_name} as: {filename} \n'

    @staticmethod
    def log_failed_song_download(song: str):
        return f"{song}'s instrumental could not be found"

    @staticmethod
    def verbose_finished_message(song_count: int, download_elapsed: str, conversion_elapsed: str, elapsed: str):
        """
        Returns the verbose message that is printed on completion of all downloads, conversions, and renaming.

        :param song_count: The amount of songs that finished
        :param download_elapsed: The time that elapsed during the download process
        :param conversion_elapsed: The time that elapsed during the conversion and renaming process
        :param elapsed: The full time that elapsed during the process
        :return: The final verbose message
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
        """
        Return's an 's' for pluralization if the amount of songs downloaded is greater than 1

        :param song_count: The amount of songs that finished
        :return: Either a blank character '' or 's'
        """
        if song_count == 1:
            return ''
        return 's'
