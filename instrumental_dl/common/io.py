import os

from ..errors import UnknownExtensionError


def get_songs_txt(file_name: str):
    """
    Opens up the provided text file to retrieve a list of all
    the instrumentals that are going to be downloaded.

    :param file_name: The name of the file that contains
                      a list of all the instrumentals to be downloaded.
    :return: song_names: A list of the names of all of the instrumentals
                         to be downloaded.
    """
    with open(file_name, "r") as file:
        song_names = [song.rstrip('\n') for song in file]
    return song_names


def rename_all_files(file_names: list):
    """
    Renames all downloaded instrumentals to remove any unneeded
    keywords in the file name.

    :param file_names: A list of the names of all the downloaded files.
                       file_names do not need to have .mp3 as their extension
                       when passed through.
    """
    # Move to output directory
    os.chdir(os.getcwd() + '/../output')
    keywords = _get_keywords()

    for file_name in file_names:
        # Replaces extension in file_name(not actual file name) to .mp3
        if file_name[-5:] == '.webm':
            file_name = file_name.replace('.webm', '.mp3')
        elif file_name[-4:] == '.m4a':
            file_name = file_name.replace('.m4a', '.mp3')
        else:
            raise UnknownExtensionError(file_name)

        # Removes any unneeded keywords in actual file name
        for keyword in keywords:
            if keyword in file_name:
                try:
                    os.rename(file_name, file_name.replace(keyword, ''))
                    break
                except FileNotFoundError:
                    print("Error:", file_name, "not found.")


def _get_keywords():
    """
    Opens keywords.txt and retrieves all the keywords to
    remove from file names.

    :return: keywords: A list of all the keywords to remove
                       file names.
    """
    keywords = []
    with open('../config/keywords.txt', 'r') as file:
        for keyword in file:
            keywords.append(keyword)

    return keywords
