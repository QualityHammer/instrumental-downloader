def read_txt_file(file_name: str):
    with open(file_name, "r") as file:
        song_names = [song.rstrip('\n') for song in file]
    return song_names
