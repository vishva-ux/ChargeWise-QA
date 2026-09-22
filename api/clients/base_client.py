"""
Base HTTP API Client providing session management, logging, and Allure request/response attachments.
"""
import requests
import json
import logging
from typing import Dict, Any, Optional
import allure

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Base REST API client wrapping requests.Session."""

    def __init__(self, base_url: str, timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def set_auth_token(self, token: str) -> None:
        """Sets Bearer authorization token header."""
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_auth_token(self) -> None:
        """Removes authorization header."""
        self.session.headers.pop("Authorization", None)

    def _attach_allure(self, method: str, url: str, headers: Dict, payload: Any, response: requests.Response) -> None:
        """Attaches HTTP request and response details to Allure report."""
        try:
            req_info = (
                f"METHOD: {method}\n"
                f"URL: {url}\n"
                f"HEADERS: {json.dumps(dict(headers), indent=2)}\n"
                f"PAYLOAD: {json.dumps(payload, indent=2) if payload else 'None'}"
            )
            allure.attach(req_info, name=f"HTTP Request [{method}]", attachment_type=allure.attachment_type.TEXT)

            res_info = (
                f"STATUS: {response.status_code}\n"
                f"ELAPSED: {response.elapsed.total_seconds():.3f}s\n"
                f"BODY:\n{response.text}"
            )
            allure.attach(res_info, name=f"HTTP Response [{response.status_code}]", attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: Optional[int] = None
    ) -> requests.Response:
        """Dispatches an HTTP request with logging and optional status code assertion."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        merged_headers = {**self.session.headers, **(headers or {})}

        logger.info(f"API Request: {method} {url} | Params: {params} | JSON: {json_data}")
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json_data,
            headers=merged_headers,
            timeout=self.timeout
        )

        logger.info(f"API Response: {response.status_code} in {response.elapsed.total_seconds():.3f}s")
        self._attach_allure(method, url, merged_headers, json_data or data, response)

        if expected_status is not None:
            assert response.status_code == expected_status, (
                f"Expected status {expected_status} for {method} {url}, got {response.status_code}. "
                f"Body: {response.text}"
            )

        return response

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, json_data=json_data, **kwargs)

    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, json_data=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)
