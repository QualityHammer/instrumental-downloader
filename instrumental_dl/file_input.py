from logging import getLogger


def read_songs_txt(file_path: str) -> list:
    getLogger("file_input").debug(f"Reading songs from {file_path}.")
    with open(file_path, 'r') as file:
        return [song.rstrip() for song in file]
