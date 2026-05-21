"""GitHub REST API v3 client — repos, issues, pull requests, commits.

Reads GITHUB_TOKEN from environment. Never hardcoded.

Usage:
    from claude_connectors.github import GitHubClient
    gh = GitHubClient.from_env()
    repo = gh.get_repo("your-org", "your-repo")
    issues = gh.list_issues("your-org", "your-repo", state="open")

Reversibility:
- GET (repo, issues, PRs, commits) are Y
- POST/PATCH/PUT/DELETE (create issue, create PR, merge, release) are N — operator confirm

Setup: github.com/settings/tokens -> generate personal access token (classic or fine-grained)
with the scopes you need (repo, read:user, etc.).
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

BASE_URL = "https://api.github.com"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
API_VERSION = "2022-11-28"


class GitHubError(Exception):
    pass


@dataclass
class WriteRequest:
    method: str
    path: str
    body: dict[str, Any]
    description: str


class GitHubClient:
    def __init__(self, token: str, *, timeout: int = DEFAULT_TIMEOUT) -> None:
        if not token:
            raise ValueError("GitHubClient requires a non-empty token")
        self._token = token
        self._timeout = timeout

    @classmethod
    def from_env(cls, *, env_var: str = "GITHUB_TOKEN") -> "GitHubClient":
        tok = os.environ.get(env_var)
        if not tok:
            raise GitHubError(f"{env_var} is not set. Generate a PAT at github.com/settings/tokens.")
        return cls(token=tok)

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        url = f"{BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "ROOK-GitHub-Client/1.0",
        }
        data: bytes | None = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        last_err: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                req = Request(url, data=data, headers=headers, method=method)
                with urlopen(req, timeout=self._timeout) as resp:
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw) if raw else {}
            except HTTPError as e:
                if e.code in (429, 403) and "rate limit" in e.reason.lower() and attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt * 30)  # GitHub rate-limits reset on the minute
                    continue
                if 400 <= e.code < 500:
                    try:
                        detail = json.loads(e.read().decode("utf-8"))
                    except Exception:
                        detail = {"raw": "<unparseable>"}
                    raise GitHubError(f"HTTP {e.code} on {method} {path}: {detail}") from e
                last_err = e
            except URLError as e:
                last_err = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
        raise GitHubError(f"Request failed after {MAX_RETRIES} attempts: {last_err}")

    # ---- Reads (Y) ----

    def get_repo(self, owner: str, repo: str) -> dict[str, Any]:
        return self._request("GET", f"/repos/{owner}/{repo}")

    def list_issues(
        self,
        owner: str,
        repo: str,
        *,
        state: str = "open",
        labels: str | None = None,
        per_page: int = 30,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"state": state, "per_page": per_page}
        if labels:
            params["labels"] = labels
        path = f"/repos/{owner}/{repo}/issues?{urlencode(params)}"
        return self._request("GET", path)

    def get_issue(self, owner: str, repo: str, number: int) -> dict[str, Any]:
        return self._request("GET", f"/repos/{owner}/{repo}/issues/{number}")

    def list_pulls(
        self,
        owner: str,
        repo: str,
        *,
        state: str = "open",
        per_page: int = 30,
    ) -> list[dict[str, Any]]:
        path = f"/repos/{owner}/{repo}/pulls?{urlencode({'state': state, 'per_page': per_page})}"
        return self._request("GET", path)

    def get_pull(self, owner: str, repo: str, number: int) -> dict[str, Any]:
        return self._request("GET", f"/repos/{owner}/{repo}/pulls/{number}")

    def list_commits(self, owner: str, repo: str, *, per_page: int = 30) -> list[dict[str, Any]]:
        path = f"/repos/{owner}/{repo}/commits?{urlencode({'per_page': per_page})}"
        return self._request("GET", path)

    def get_user(self) -> dict[str, Any]:
        return self._request("GET", "/user")

    # ---- Writes (N — gated) ----

    def prepare_issue_create(self, owner: str, repo: str, title: str, *, body: str = "", labels: list[str] | None = None) -> WriteRequest:
        payload: dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        return WriteRequest(
            method="POST",
            path=f"/repos/{owner}/{repo}/issues",
            body=payload,
            description=f"Create issue in {owner}/{repo}: '{title[:60]}'",
        )

    def prepare_issue_close(self, owner: str, repo: str, number: int) -> WriteRequest:
        return WriteRequest(
            method="PATCH",
            path=f"/repos/{owner}/{repo}/issues/{number}",
            body={"state": "closed"},
            description=f"Close issue {owner}/{repo}#{number}",
        )

    def prepare_pull_merge(self, owner: str, repo: str, number: int, *, commit_title: str | None = None) -> WriteRequest:
        payload: dict[str, Any] = {}
        if commit_title:
            payload["commit_title"] = commit_title
        return WriteRequest(
            method="PUT",
            path=f"/repos/{owner}/{repo}/pulls/{number}/merge",
            body=payload,
            description=f"Merge PR {owner}/{repo}#{number}",
        )

    def execute_write(self, write: WriteRequest, *, confirmed: bool = False) -> dict[str, Any]:
        if not confirmed:
            raise GitHubError(
                f"Write blocked — `confirmed=True` not set. Description: {write.description}"
            )
        return self._request(write.method, write.path, write.body)
