class MKBaseException(Exception):
    def __init__(self, message: str = None, **kwargs) -> None:
        self.message = message
        super().__init__(message, **kwargs)


class MKFrontendException(MKBaseException):
    pass

class MKInvalidInputException(MKFrontendException):
    pass
