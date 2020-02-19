from logging import getLogger
from os import rename
from os.path import join, dirname, realpath

from instrumental_dl.exceptions import DownloadNotFoundException


def rename_all_files(file_names: list, verbose: bool):
    logger = getLogger("file_names")
    keywords = _get_keywords()

    for i in range(len(file_names)):
        old_file_name = file_names[i]

        if file_names[i][-5:] == '.webm':
            file_names[i] = file_names[i].replace('.webm', '.mp3')
        elif file_names[i][-4:] == '.m4a':
            file_names[i] = file_names[i].replace('.m4a', '.mp3')

        for keyword in keywords:
            if keyword in file_names[i].lower():
                new_file_name = file_names[i].lower().replace(keyword, '').capitalize()
                try:
                    rename(file_names[i], new_file_name)
                except FileNotFoundError:
                    logger.error(str(DownloadNotFoundException(file_names[i])))
                except FileExistsError:
                    new_file_name = _file_recursion_creator(old_file_name,
                                                            new_file_name[:-4])
                file_names[i] = new_file_name

            while file_names[i][-5] == ' ' or file_names[i][-5] == '-':
                new_file_name = f"{file_names[i][:-5]}.mp3"
                try:
                    rename(file_names[i], new_file_name)
                except FileNotFoundError:
                    logger.error(str(DownloadNotFoundException(file_names[i])))
                except FileExistsError:
                    new_file_name = _file_recursion_creator(file_names[i], new_file_name[:-4])
                file_names[i] = new_file_name
        log = f"Renamed {old_file_name} to {file_names[i]}."
        logger.info(log)
        if verbose:
            print(log)


def _file_recursion_creator(old_file_name: str, new_file_name: str,
                            recursion_count: int = 1) -> str:
    new_file_name += f"({recursion_count}.mp3"
    try:
        rename(old_file_name, new_file_name)
    except FileExistsError:
        new_file_name = _file_recursion_creator(old_file_name, new_file_name[:-7],
                                                recursion_count + 1)

    return new_file_name


def _get_keywords() -> list:
    key_path = join(dirname(dirname(realpath(__file__))), "config", "keywords")
    keywords = []
    with open(key_path, 'r') as file:
        for keyword in file:
            keywords.append(keyword.rstrip('\n'))

    return keywords
