class InvalidType(Exception):
    def __init__(self, msg="Field is of unknown type", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class NotFoundError(Exception):
    pass
