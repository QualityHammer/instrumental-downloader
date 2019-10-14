import os
import platform

from .args import is_verbose
from ..errors import UnknownExtensionError


def rename_all_files(logger, file_names: list):
    """
    Renames all downloaded instrumentals to remove any unneeded
    keywords in the file name.

    :param logger: The main logger for this program
    :param file_names: A list of the names of all the downloaded files.
                       file_names do not need to have .mp3 as their extension
                       when passed through.
    """
    if is_verbose():
        print('Starting renaming process...')

    keywords = _get_keywords()

    for i in range(len(file_names)):
        old_name = None
        if is_verbose():
            old_name = file_names[i]

        # Replaces extension in file_name(not actual file name) to .mp3
        if file_names[i][-5:] == '.webm':
            file_names[i] = file_names[i].replace('.webm', '.mp3')
        elif file_names[i][-4:] == '.m4a':
            file_names[i] = file_names[i].replace('.m4a', '.mp3')
        else:
            raise UnknownExtensionError(logger, file_names[i])

        # Removes any unneeded keywords in actual file name
        for keyword in keywords:
            if keyword in file_names[i].lower():
                try:
                    new_file_name = file_names[i].lower().replace(keyword, '').capitalize()
                    os.rename(file_names[i], new_file_name)
                    file_names[i] = new_file_name
                except FileNotFoundError:
                    _file_error(logger, file_names[i])

        # Removes unneeded space at the end of file name
        while file_names[i][-5] == ' ' or file_names[i][-5] == '-':
            try:
                new_file_name = file_names[i][:-5] + '.mp3'
                os.rename(file_names[i], new_file_name)
                file_names[i] = new_file_name
            except FileNotFoundError:
                _file_error(logger, file_names[i])

        if is_verbose():
            print(f'Converted and renamed {old_name} to {file_names[i]}.')


def _file_error(logger, file_name):
    """Handles FileNotFoundErrors"""
    msg = f"Error: {file_name} not found."
    logger.error(msg)
    print(msg)


def _get_keywords():
    """
    Opens keywords.txt and retrieves all the keywords to
    remove from file names.

    :return: keywords: A list of all the keywords to remove
                       file names.
    """
    if platform.system() == 'Windows':
        key_file = 'config\\keywords.txt'
    else:
        key_file = 'config/keywords.txt'
    key_path = os.path.join(os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__))),
        key_file)

    keywords = []
    with open(key_path, 'r') as file:
        for keyword in file:
            keywords.append(keyword.rstrip('\n'))

    return keywords
