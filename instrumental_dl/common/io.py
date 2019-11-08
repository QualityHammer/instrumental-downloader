import os
import platform

from .args import ArgHandler
from ..errors import UnknownExtensionError


def rename_all_files(logger):
    """
    Renames all downloaded instrumentals to remove any unneeded
    keywords in the file name.

    :param: logger -- The main logger for this program

    :var: file_names -- A list of the names of all the downloaded files.
                       file_names do not need to have .mp3 as their extension
                       when passed through.
    """
    if ArgHandler.is_verbose() and len(logger.song_titles) > 0:
        print('Starting renaming process...')

    keywords = _get_keywords()
    file_names = logger.file_names

    for i in range(len(file_names)):
        old_name = None
        if ArgHandler.is_verbose():
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
                new_file_name = file_names[i].lower().replace(keyword, '').capitalize()
                try:
                    os.rename(file_names[i], new_file_name)
                    file_names[i] = new_file_name
                except FileNotFoundError:
                    _no_file_error(logger, file_names[i])
                except FileExistsError:
                    replacement = _file_recursion_creator(file_names[i],  new_file_name[:-4])
                    _file_exists_error(logger, file_names[i], replacement, new_file_name)
                    file_names[i] = replacement

        # Removes unneeded space at the end of file name
        while file_names[i][-5] == ' ' or file_names[i][-5] == '-':
            new_file_name = file_names[i][:-5] + '.mp3'
            try:
                os.rename(file_names[i], new_file_name)
                file_names[i] = new_file_name
            except FileNotFoundError:
                _no_file_error(logger, file_names[i])
            except FileExistsError:
                replacement = _file_recursion_creator(file_names[i],  new_file_name[:-4])
                _file_exists_error(logger, file_names[i], replacement, new_file_name)
                file_names[i] = replacement

        if ArgHandler.is_verbose():
            print(f'Converted and renamed {old_name} to {file_names[i]}.')


def _file_recursion_creator(old_file_name: str, new_file_name: str, n: int = 1):
    """If a file cannot be renamed because of a FileExistsError, it calls this recursive
    function which calls itself until it can rename the file to a name that doesn't exist.

    :param: old_file_name --  The name of the file that is attempting to be renamed.
    :param: new_file_name -- What the file will be renamed to in this function.
    :param: n -- The number of existing files that exist.

    :return: The attempted renamed file.
    """
    new_file_name += f"({n}).mp3"
    try:
        os.rename(old_file_name, new_file_name)
    except FileExistsError:
        new_file_name = _file_recursion_creator(old_file_name, new_file_name[:-7], n + 1)

    return new_file_name


def _no_file_error(logger, file_name):
    """Handles FileNotFoundErrors"""
    msg = f"{file_name} not found."
    logger.error(msg)
    print(msg)


def _file_exists_error(logger, old_file_name, new_file_name, existing_file_name):
    """Handles FileExistsErrors"""
    msg = f"\nINFO\n  - Tried to rename {old_file_name} to {existing_file_name}, but it " \
        f"already exists. It was instead renamed to {new_file_name}"
    logger.warning(msg)
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
