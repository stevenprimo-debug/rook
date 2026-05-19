"""Stripe API client — payments, subscriptions, customers, balance.

Reads STRIPE_API_KEY from environment (use sk_live_... or sk_test_... — env vars
STRIPE_API_KEY_LIVE and STRIPE_API_KEY_TEST both supported).

Usage:
    from claude_connectors.stripe import StripeClient
    s = StripeClient.from_env()
    bal = s.get_balance()
    subs = s.list_subscriptions(status="active")

Reversibility:
- GET (list, retrieve) are Y
- POST/DELETE (charge, refund, subscription create/cancel) are N — operator confirm via prepare_X / execute_write

Setup: dashboard.stripe.com/apikeys -> restrict key to needed scopes only.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://api.stripe.com/v1"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3


class StripeError(Exception):
    pass


@dataclass
class WriteRequest:
    method: str
    path: str
    body: dict[str, Any]
    description: str


class StripeClient:
    def __init__(self, api_key: str, *, timeout: int = DEFAULT_TIMEOUT) -> None:
        if not api_key:
            raise ValueError("StripeClient requires a non-empty api_key")
        self._key = api_key
        self._timeout = timeout

    @classmethod
    def from_env(
        cls,
        *,
        env_var: str = "STRIPE_API_KEY",
        live_env_var: str = "STRIPE_API_KEY_LIVE",
        test_env_var: str = "STRIPE_API_KEY_TEST",
        prefer_test: bool = False,
    ) -> "StripeClient":
        # Priority: explicit STRIPE_API_KEY > test/live based on prefer_test
        key = os.environ.get(env_var)
        if not key:
            if prefer_test:
                key = os.environ.get(test_env_var) or os.environ.get(live_env_var)
            else:
                key = os.environ.get(live_env_var) or os.environ.get(test_env_var)
        if not key:
            raise StripeError(
                f"No Stripe key found. Set {env_var} (or {live_env_var}/{test_env_var})."
            )
        return cls(api_key=key)

    @property
    def is_test_mode(self) -> bool:
        return self._key.startswith("sk_test_")

    def _request(self, method: str, path: str, form: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = urlencode(form).encode("utf-8") if form is not None else None

        last_err: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                req = Request(url, data=data, headers=headers, method=method)
                with urlopen(req, timeout=self._timeout) as resp:
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw) if raw else {}
            except HTTPError as e:
                if e.code == 429 and attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
                if 400 <= e.code < 500:
                    try:
                        detail = json.loads(e.read().decode("utf-8"))
                    except Exception:
                        detail = {"raw": "<unparseable>"}
                    raise StripeError(f"HTTP {e.code} on {method} {path}: {detail}") from e
                last_err = e
            except URLError as e:
                last_err = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
        raise StripeError(f"Request failed after {MAX_RETRIES} attempts: {last_err}")

    # ---- Reads (Y) ----

    def get_balance(self) -> dict[str, Any]:
        return self._request("GET", "/balance")

    def list_customers(self, *, limit: int = 100, email: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if email:
            params["email"] = email
        path = f"/customers?{urlencode(params)}"
        return self._request("GET", path).get("data", [])

    def list_charges(self, *, limit: int = 100) -> list[dict[str, Any]]:
        path = f"/charges?limit={limit}"
        return self._request("GET", path).get("data", [])

    def list_subscriptions(self, *, limit: int = 100, status: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if status:
            params["status"] = status
        path = f"/subscriptions?{urlencode(params)}"
        return self._request("GET", path).get("data", [])

    def list_invoices(self, *, limit: int = 100, customer: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if customer:
            params["customer"] = customer
        path = f"/invoices?{urlencode(params)}"
        return self._request("GET", path).get("data", [])

    # ---- Writes (N — gated) ----

    def prepare_refund(self, charge_id: str, *, amount: int | None = None, reason: str | None = None) -> WriteRequest:
        body: dict[str, Any] = {"charge": charge_id}
        if amount is not None:
            body["amount"] = amount
        if reason:
            body["reason"] = reason
        return WriteRequest(
            method="POST",
            path="/refunds",
            body=body,
            description=f"Refund charge {charge_id}" + (f" amount={amount}" if amount else " (full)"),
        )

    def prepare_subscription_cancel(self, subscription_id: str) -> WriteRequest:
        return WriteRequest(
            method="DELETE",
            path=f"/subscriptions/{subscription_id}",
            body={},
            description=f"Cancel subscription {subscription_id}",
        )

    def execute_write(self, write: WriteRequest, *, confirmed: bool = False) -> dict[str, Any]:
        if not confirmed:
            raise StripeError(
                f"Write blocked — `confirmed=True` not set. Description: {write.description}"
            )
        return self._request(write.method, write.path, write.body)
