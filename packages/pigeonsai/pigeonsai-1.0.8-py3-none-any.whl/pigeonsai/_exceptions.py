from __future__ import annotations

from typing import Any, Optional, cast
from typing_extensions import Literal

import httpx

from ._utils import is_dict

__all__ = [
    "PigeonsAIError",
    "APIError",
    "APIStatusError",
    "APIResponseValidationError",
    "APIConnectionError",
    "APITimeoutError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
]


class PigeonsAIError(Exception):
    pass


class APIError(PigeonsAIError):
    """A base class for API errors, capturing common attributes."""

    message: str
    body: object | None
    code: Optional[str]
    param: Optional[str]
    type: Optional[str]

    def __init__(self, message: str, *, body: object | None) -> None:
        super().__init__(message)
        self.message = message
        self.body = body

        if is_dict(body):
            self.code = cast(Any, body.get("code"))
            self.param = cast(Any, body.get("param"))
            self.type = cast(Any, body.get("type"))
        else:
            self.code = None
            self.param = None
            self.type = None


class APIResponseValidationError(APIError):
    """Raised for validation errors of the API response against the expected schema."""

    response: httpx.Response
    status_code: int

    def __init__(self, response: httpx.Response, body: object | None, *, message: str | None = None) -> None:
        super().__init__(message or "Data returned by API is invalid for the expected schema.", response.request, body=body)
        self.response = response
        self.status_code = response.status_code


class APIStatusError(APIError):
    """Raised for API responses with status codes of 4xx or 5xx."""

    response: httpx.Response
    status_code: int

    def __init__(self, message: str, *, response: httpx.Response, body: object | None) -> None:
        super().__init__(message, body=body)
        self.response = response
        self.status_code = response.status_code


class APIConnectionError(APIError):
    """Raised for errors encountered while trying to connect to the API."""

    def __init__(self, *, message: str = "Connection error.", request: httpx.Request) -> None:
        super().__init__(message, request, body=None)


class APITimeoutError(APIConnectionError):
    """Raised for request timeouts."""

    def __init__(self, request: httpx.Request) -> None:
        super().__init__(message="Request timed out.", request=request)


# Specific status errors follow the same structure as OpenAI's exceptions
class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400


class AuthenticationError(APIStatusError):
    status_code: Literal[401] = 401


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403] = 403


class NotFoundError(APIStatusError):
    status_code: Literal[404] = 404


class ConflictError(APIStatusError):
    status_code: Literal[409] = 409


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422] = 422


class RateLimitError(APIStatusError):
    status_code: Literal[429] = 429


class InternalServerError(APIStatusError):
    status_code: Literal[500] = 500
