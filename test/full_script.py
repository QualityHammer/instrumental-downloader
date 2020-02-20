from argparse import Namespace
from os.path import join, expanduser

from instrumental_dl.client import run
from instrumental_dl.__version__ import __version__


class SongArgs1(Namespace):
    def __init__(self):
        Namespace.__init__(self)
        self.file = None
        self.output = None
        self.songs = ["\"mf doom doomsday\""]
        self.verbose = True


class SongArgs2(Namespace):
    def __init__(self):
        Namespace.__init__(self)
        self.file = None
        self.output = join(expanduser('~'), "Instrumentals")
        self.songs = ["\"wu tang clan triumph\"",
                "\"gang starr meaning of the name\"",
                "\"snoop dogg gold rush\""]
        self.verbose = False


def test_full_script():
    assert run(SongArgs1()) == None
    assert run(SongArgs2()) == None

