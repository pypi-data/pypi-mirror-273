from typing import NoReturn, Any


class ClientException(Exception):
    def __init__(self, endpoint: str, status_code: int, response_content: bytes) -> NoReturn:
        self.endpoint: str = endpoint
        self.status_code: int = status_code
        self.response_content: bytes = response_content

    def __str__(self) -> str:
        return f"Request to {self.endpoint} unsuccessful. Status code: {self.status_code}. Response content: {self.response_content}"

    def __repr__(self) -> str:
        return "<ClientException(endpoint='%s', status_code=%s, response_content='%s')>" % (
            self.endpoint,
            self.status_code,
            self.response_content,
        )


class InvalidParamsException(Exception):
    def __init__(self, message: str, key: str, value: Any) -> NoReturn:
        self.message: str = message
        self.key: str = key
        self.value: str = value

    def __str__(self) -> str:
        return f"Invalid params for {self.key}: {self.value}. Message: {self.message}"

    def __repr__(self) -> str:
        return "<InvalidParams(message='%s', key='%s', value=%s)>" % (self.message, self.key, repr(self.value))
