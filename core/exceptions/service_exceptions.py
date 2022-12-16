class AlreadyExistsError(Exception):
    """
    An exception to indicate that we already created this record
    """
    def __init__(self, message: str = None) -> None:
        self.message = message