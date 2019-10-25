class BaseError(Exception):
    """Base exception"""

    def __init__(self, msg, logger):
        Exception.__init__(self, msg)
        logger.error(msg)


class UnknownExtensionError(BaseError):
    """Exception for when youtube-dl downloads an instrumental in
    an unknown extension which needs to be added to the program.

    Attributes:
        file_name -- The file name for the file with the unknown exception
        message -- Explanation of what to do when this error occurs.
    """

    def __init__(self, logger, file_name: str):
        self.file_name = file_name
        self.message = "The extension in " + file_name + \
                       " is unknown and needs to be added by the developer"
        BaseError.__init__(self, self.message, logger)
