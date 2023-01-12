class UnprocessableError(Exception):
    """
    An exception to indicate the data cannot be processed as provided
    """

    def __init__(self, message: str = None) -> None:
        self.message = message


class NotFoundError(Exception):
    pass
