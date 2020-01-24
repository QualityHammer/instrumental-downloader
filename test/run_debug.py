from argparse import Namespace

from instrumental_dl.client import run


class DebugArguments(Namespace):
    def __init__(self):
        Namespace.__init__(self)
        self.s = ["\"mf doom doomsday\""]
        self.v = True


if __name__ == "__main__":
    run(DebugArguments())
