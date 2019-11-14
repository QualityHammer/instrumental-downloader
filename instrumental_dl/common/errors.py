from instrumental_dl.logger import Logger


class BaseError(Exception):
    """Base exception

    Parameters
    ----------
    logger: Logger
        The main logger object for the process
    msg: str
        The message that is printed to the console on an error.
    """

    def __init__(self, msg, logger):
        Exception.__init__(self, msg)
        logger.error(msg)


class UnknownExtensionError(BaseError):
    """Exception for when youtube-dl downloads an instrumental in
    an unknown extension which needs to be added to the program.

    Parameters
    ----------
    logger: Logger
        The main logger object for the process
    file_name: str
        The file name for the file with the unknown exception
    """

    def __init__(self, logger: Logger, file_name: str):
        """
        Attribute
        ---------
        message: str
            Explanation of what to do when this error occurs.
        """
        self.file_name = file_name
        self.message = "The extension in " + file_name + \
                       " is unknown and needs to be added by the developer"
        BaseError.__init__(self, self.message, logger)


class NoInternetConnectionError(BaseError):
    """This exception is raised if there is no internet access available.

    Parameter
    ---------
    logger: Logger
        The main logger object for the process
    """

    def __init__(self, logger):
        self.message = "An internet connection could not be found. Check your " \
                        "network settings to make sure you're connected to a network."
        BaseError.__init__(self, self.message, logger)


class NoInstrumentalFoundError(BaseError):
    """This exception is raised if a search for an instrumental comes back
    with 0 video results.
    
    Parameters
    ----------
    logger: Logger
        The main logger object for the process
    song_name: str
        The name of the song that had no results
    """

    def __init__(self, logger: Logger, song_name: str):
        self.message = f"There were no results for {song_name} Instrumental."
        BaseError.__init__(self, self.message, logger)
