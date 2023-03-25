import requests


class PrincessException(Exception):
    pass


class HTTPException(Exception):
    def __init__(self, response, *, response_json=None) -> None:
        self.response = response
        try:
            status_code = response.status_code
        except AttributeError:
            status_code = response.status

        if response_json is None:
            try:
                response_json = response.json()
            except requests.JSONDecodeError:
                super().__init__(f"{status_code} {response.reason}")
                return

        super().__init__(f"{status_code} {response.reason}")


class BadRequest(HTTPException):
    pass


class NotFound(HTTPException):
    pass


class ServerError(HTTPException):
    pass


