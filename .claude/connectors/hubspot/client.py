"""HubSpot CRM API client — deals, contacts, companies.

Reads HUBSPOT_PRIVATE_APP_TOKEN from environment. Never hardcoded.

Usage:
    from claude_connectors.hubspot import HubSpotClient
    hs = HubSpotClient.from_env()
    deals = hs.list_deals(stage="contractsent", limit=50)
    for d in deals:
        print(d["id"], d["properties"]["dealname"])

Reversibility:
- GET (list, get) are Y (autonomous)
- PATCH on deal stage / contact properties are N (operator confirm required)
- POST/DELETE are N

Setup: HubSpot Admin -> Integrations -> Private Apps -> create app with scopes
crm.objects.contacts.read/write, crm.objects.deals.read/write, crm.objects.companies.read/write.
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

BASE_URL = "https://api.hubapi.com"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3


class HubSpotError(Exception):
    pass


@dataclass
class WriteRequest:
    """Pending write — never executed without explicit confirm."""
    method: str
    path: str
    body: dict[str, Any]
    description: str


class HubSpotClient:
    def __init__(self, token: str, *, timeout: int = DEFAULT_TIMEOUT) -> None:
        if not token:
            raise ValueError("HubSpotClient requires a non-empty token")
        self._token = token
        self._timeout = timeout

    @classmethod
    def from_env(cls, *, env_var: str = "HUBSPOT_PRIVATE_APP_TOKEN") -> "HubSpotClient":
        tok = os.environ.get(env_var)
        if not tok:
            raise HubSpotError(f"{env_var} is not set. Create a Private App at HubSpot Admin > Integrations.")
        return cls(token=tok)

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        data = json.dumps(body).encode("utf-8") if body is not None else None

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
                    raise HubSpotError(f"HTTP {e.code} on {method} {path}: {detail}") from e
                last_err = e
            except URLError as e:
                last_err = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
        raise HubSpotError(f"Request failed after {MAX_RETRIES} attempts: {last_err}")

    # ---- Reads (autonomous, reversibility=Y) ----

    def list_deals(
        self,
        *,
        stage: str | None = None,
        limit: int = 100,
        properties: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if properties:
            params["properties"] = ",".join(properties)
        path = f"/crm/v3/objects/deals?{urlencode(params)}"
        result = self._request("GET", path)
        deals = result.get("results", [])
        if stage:
            deals = [d for d in deals if d.get("properties", {}).get("dealstage") == stage]
        return deals

    def get_deal(self, deal_id: str, *, properties: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, str] = {}
        if properties:
            params["properties"] = ",".join(properties)
        path = f"/crm/v3/objects/deals/{deal_id}"
        if params:
            path += f"?{urlencode(params)}"
        return self._request("GET", path)

    def list_contacts(self, *, limit: int = 100, properties: list[str] | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if properties:
            params["properties"] = ",".join(properties)
        path = f"/crm/v3/objects/contacts?{urlencode(params)}"
        return self._request("GET", path).get("results", [])

    def get_contact(self, contact_id: str, *, properties: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, str] = {}
        if properties:
            params["properties"] = ",".join(properties)
        path = f"/crm/v3/objects/contacts/{contact_id}"
        if params:
            path += f"?{urlencode(params)}"
        return self._request("GET", path)

    # ---- Writes (gated, reversibility=N — return WriteRequest for operator confirm) ----

    def prepare_deal_stage_update(self, deal_id: str, new_stage: str) -> WriteRequest:
        """Return a WriteRequest. Caller must explicitly invoke execute_write() with operator confirm."""
        return WriteRequest(
            method="PATCH",
            path=f"/crm/v3/objects/deals/{deal_id}",
            body={"properties": {"dealstage": new_stage}},
            description=f"Update deal {deal_id} dealstage -> {new_stage}",
        )

    def prepare_contact_update(self, contact_id: str, properties: dict[str, str]) -> WriteRequest:
        return WriteRequest(
            method="PATCH",
            path=f"/crm/v3/objects/contacts/{contact_id}",
            body={"properties": properties},
            description=f"Update contact {contact_id} properties: {list(properties.keys())}",
        )

    def execute_write(self, write: WriteRequest, *, confirmed: bool = False) -> dict[str, Any]:
        """Execute a prepared WriteRequest. `confirmed=True` MUST be set explicitly by the operator."""
        if not confirmed:
            raise HubSpotError(
                f"Write blocked — `confirmed=True` not set. Description: {write.description}"
            )
        return self._request(write.method, write.path, write.body)
