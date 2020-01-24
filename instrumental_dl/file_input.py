def read_songs_txt(file_path: str) -> list:
    with open(file_path, 'r') as file:
        return [song.rstrip() for song in file]
