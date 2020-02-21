from logging import getLogger


def read_songs_txt(file_path: str) -> list:
    """Reads a list of songs to download from a text file.

    Parameters:
      file_path -- the path to the file being read

    Returns:
      a list of songs to download
    """
    getLogger("file_input").debug(f"Reading songs from {file_path}.")
    with open(file_path, 'r') as file:
        return [song.rstrip() for song in file]
