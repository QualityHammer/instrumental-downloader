CONTACT_DEV_MSG = "This should not occur, so contact the developer with this issue " \
                  "if possible."


class _IdlException(Exception):

    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class DownloadNotFoundException(_IdlException):

    def __init__(self, filename: str):
        self.filename = filename
        message = f"The downloaded file; {self.filename} could not be found." \
                  f"\n      {CONTACT_DEV_MSG}"
        _IdlException.__init__(self, message)


class HelpFileNotFoundException(_IdlException):

    def __init__(self):
        message = f"The help file could not be found.\n     {CONTACT_DEV_MSG}"
        _IdlException.__init__(self, message)
