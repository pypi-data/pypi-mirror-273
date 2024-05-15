# _client.py
from __future__ import annotations

import logging
import os
from typing import Optional
import httpx
from httpx import Response, Timeout

from .resources import Recommender, AnomalyDetector, DataConnector
from . import _exceptions

__all__ = [
    "PigeonsAI",
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('')
logging.getLogger("httpx").setLevel(logging.WARNING)


class PigeonsAI:
    recommender: Recommender
    anomaly_detector: AnomalyDetector
    data_connector: DataConnector

    # client options
    api_key: str
    _http_client: httpx.Client

    def __init__(self, api_key: str | None = None) -> None:
        if api_key is None:
            api_key = os.environ.get("PIGEONSAI_API_KEY")
        if api_key is None:
            raise _exceptions.PigeonsAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the PIGEONSAI_API_KEY environment variable"
            )
        self.api_key = api_key
        self._http_client = httpx.Client(timeout=Timeout(300.0))

        self.recommender = Recommender(self)
        self.data_connector = DataConnector(self)
        self.anomaly_detector = AnomalyDetector()

    @property
    def auth_headers(self) -> dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': self.api_key,
        }

    def _handle_response(self, response: Response) -> dict:
        try:
            response.raise_for_status()
            return response
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {e}")
            raise _exceptions.RequestError("Request timed out") from e
        except httpx.HTTPStatusError as e:
            error_detail = ""
            error_body = None
            try:
                error_body = e.response.json()
                error_detail = error_body.get('message', '')
            except Exception as parse_error:
                logger.error(f"Error parsing error response body: {parse_error}")

            logger.error(f"Status code: {e.response.status_code}. Detail: {error_detail}")

            if e.response.status_code == 400:
                raise _exceptions.BadRequestError(
                    f"Bad request: {error_detail}", response=e.response, body=error_body) from e
            elif e.response.status_code == 401:
                raise _exceptions.AuthenticationError(
                    f"Authentication failed: {error_detail}", response=e.response, body=error_body) from e
            elif e.response.status_code == 404:
                raise _exceptions.NotFoundError(
                    f"Not found: {error_detail}", response=e.response, body=error_body) from e
            elif e.response.status_code == 409:
                raise _exceptions.ConflictError(
                    f"Resource already exists: {error_detail}", response=e.response, body=error_body) from e
            elif e.response.status_code >= 500:
                raise _exceptions.InternalServerError(
                    f"Server error: {error_detail}", response=e.response, body=error_body) from e
            else:
                raise _exceptions.APIStatusError(
                    f"Unexpected error: {e}. Detail: {error_detail}", response=e.response, body=error_body) from e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise _exceptions.APIError("Unexpected error") from e

    def _request(self, method: str, url: str, headers: dict, data: Optional[dict] = None) -> dict:
        response = self._http_client.request(method, url, headers=headers, json=data)
        return self._handle_response(response)

    def close(self) -> None:
        self._http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
