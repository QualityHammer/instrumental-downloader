import os


def goto_origin(origin_path):
    """Moves current directory back to where it was when the command
    was called."""
    os.chdir(origin_path)


def goto_music():
    """Moves current directory to the user's music folder."""
    os.chdir(_get_download_path())


def goto_program():
    """Moves current directory to the instrumental_dl folder."""
    os.chdir(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__))))


def _get_download_path():
    """Uses ~/Music/Instrumentals as the primary download path.
    If the path doesn't exist, it uses (and creates if needed)
    ~/music/Instrumentals as the download path."""
    music_path = os.path.join(os.path.expanduser('~'), 'Music')
    if not os.path.exists(music_path):
        music_path = os.path.join(os.path.expanduser('~'), 'music')
        if not os.path.exists(music_path):
            os.mkdir(music_path)

    download_path = os.path.join(music_path, 'Instrumentals')
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    return download_path
