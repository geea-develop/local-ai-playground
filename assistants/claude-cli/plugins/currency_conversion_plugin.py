"""
Currency Conversion Plugin
Provides a thin adapter for external exchange-rate APIs.
"""

import json
import os
from typing import Any, Dict, Optional
from urllib import error, parse, request


class CurrencyConversionPlugin:
    """Plugin for converting currency amounts using a remote API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_seconds: int = 8,
    ):
        self.base_url = (
            base_url
            or os.getenv("CURRENCY_API_BASE_URL")
            or "https://api.exchangerate.host"
        )
        self.api_key = api_key or os.getenv("CURRENCY_API_KEY")
        self.timeout_seconds = timeout_seconds

    def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> Dict[str, Any]:
        """Convert amount from one ISO currency to another."""
        query_params = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
        }
        if self.api_key:
            query_params["access_key"] = self.api_key

        query = parse.urlencode(query_params)
        url = f"{self.base_url.rstrip('/')}/convert?{query}"
        req = request.Request(
            url=url,
            headers={"Accept": "application/json"},
            method="GET",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                payload = response.read().decode("utf-8")
                data = json.loads(payload) if payload else {}
                result = data.get("result")
                rate = data.get("info", {}).get("rate")
                return {
                    "ok": True,
                    "amount": amount,
                    "from": from_currency.upper(),
                    "to": to_currency.upper(),
                    "rate": rate,
                    "result": result,
                    "raw": data,
                }
        except error.HTTPError as exc:
            return {
                "ok": False,
                "error": f"Currency API returned HTTP {exc.code}.",
            }
        except error.URLError as exc:
            return {
                "ok": False,
                "error": f"Currency API is unreachable: {exc.reason}",
            }
        except json.JSONDecodeError:
            return {
                "ok": False,
                "error": "Currency API returned invalid JSON.",
            }

    def execute(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> Dict[str, Any]:
        """Common plugin entrypoint."""
        return self.convert(amount, from_currency, to_currency)
