import os


instrumental_keywords = [
    ' (Instrumental)',
    ' [Instrumental]',
    ' Instrumental',
    ' instrumental',
    'Instrumental',
    'instrumental'
]


def read_txt_file(file_name: str):
    with open(file_name, "r") as file:
        song_names = [song.rstrip('\n') for song in file]
    return song_names


def rename_all_files(file_names: list):
    os.chdir(os.getcwd() + '/../output')

    for file_name in file_names:
        if file_name[-5:] == '.webm':
            file_name = file_name.replace('.webm', '.mp3')
        elif file_name[-4:] == '.m4a':
            file_name = file_name.replace('.m4a', '.mp3')
        else:
            print("Error: Unknown file extension:", file_name)

        for keyword in instrumental_keywords:
            if keyword in file_name:
                try:
                    os.rename(file_name, file_name.replace(keyword, ''))
                    break
                except FileNotFoundError:
                    print("Error:", file_name, "not found.")

