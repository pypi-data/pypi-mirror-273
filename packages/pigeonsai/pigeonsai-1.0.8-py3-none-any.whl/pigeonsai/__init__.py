# __init__.py

from __future__ import annotations

from ._client import (
    PigeonsAI
)
from ._exceptions import (
    PigeonsAIError,
    APIError,
    APIStatusError,
    APIResponseValidationError,
    APIConnectionError,
    APITimeoutError,
    BadRequestError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    ConflictError,
    UnprocessableEntityError,
    RateLimitError,
    InternalServerError,
)

import sys
sys.dont_write_bytecode = True
