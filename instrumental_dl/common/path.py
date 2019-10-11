import os


def goto_origin(origin_path):
    """Moves current directory back to where it was when the command
    was called."""
    os.chdir(origin_path)


def goto_music():
    """Moves current directory to the user's music folder."""
    os.chdir(os.path.join(os.path.expanduser('~'), 'Music/Instrumentals'))


def goto_program():
    """Moves current directory to the instrumental_dl folder."""
    os.chdir(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__))))
