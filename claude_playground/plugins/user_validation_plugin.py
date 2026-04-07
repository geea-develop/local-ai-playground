"""
User Validation Plugin
Provides a thin adapter for external user validation APIs.
"""

import json
import os
from typing import Any, Dict, Optional
from urllib import error, parse, request


class UserValidationPlugin:
    """Plugin for validating user records via an external service."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_seconds: int = 8,
    ):
        self.base_url = base_url or os.getenv("USER_VALIDATION_BASE_URL")
        self.api_key = api_key or os.getenv("USER_VALIDATION_API_KEY")
        self.timeout_seconds = timeout_seconds

    def is_configured(self) -> bool:
        """Return True when a validation endpoint is configured."""
        return bool(self.base_url)

    def validate_user(self, user_id: str) -> Dict[str, Any]:
        """
        Validate a user by ID using an external endpoint.

        Expected endpoint:
        GET {base_url}/validate?user_id=<id>
        """
        if not self.base_url:
            return {
                "ok": False,
                "error": "User validation service is not configured.",
            }

        query = parse.urlencode({"user_id": user_id})
        url = f"{self.base_url.rstrip('/')}/validate?{query}"
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = request.Request(url=url, headers=headers, method="GET")
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                payload = response.read().decode("utf-8")
                data = json.loads(payload) if payload else {}
                return {"ok": True, "data": data}
        except error.HTTPError as exc:
            return {
                "ok": False,
                "error": f"Validation API returned HTTP {exc.code}.",
            }
        except error.URLError as exc:
            return {
                "ok": False,
                "error": f"Validation API is unreachable: {exc.reason}",
            }
        except json.JSONDecodeError:
            return {
                "ok": False,
                "error": "Validation API returned invalid JSON.",
            }

    def execute(self, user_id: str) -> Dict[str, Any]:
        """Common plugin entrypoint."""
        return self.validate_user(user_id)
