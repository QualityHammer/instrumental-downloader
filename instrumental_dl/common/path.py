import os


def goto_music():
    """Moves current directory to the user's music folder."""
    os.chdir(os.path.join(os.path.expanduser('~'), 'Music/Instrumentals'))


def goto_bin():
    """Moves current directory to the bin."""
    os.chdir(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__)))))
