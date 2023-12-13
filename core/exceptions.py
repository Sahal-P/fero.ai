from rest_framework import exceptions

class InternalError(exceptions.APIException):
    def __init__(self, error):
        detail = {"Internal Error Occurred": f"[{error}]"}
        if error is None:
            detail = {"Internal Error Occurred"}
        super().__init__(detail)
