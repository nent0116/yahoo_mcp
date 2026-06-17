"""HTTP client for LY/Yahoo! JAPAN Ads API."""

from collections.abc import Mapping
from typing import Any, Literal
from urllib.parse import urlencode

import httpx
from fastmcp.exceptions import ToolError

from yahoo_ads_mcp.config import YahooAdsConfig, get_config

ApiType = Literal["search", "display"]


class YahooAdsClient:
  """Small REST client for Yahoo Ads APIs."""

  def __init__(
    self,
    config: YahooAdsConfig | None = None,
    *,
    http_client: httpx.Client | None = None,
  ):
    self.config = config or get_config()
    self._client = http_client or httpx.Client(timeout=60.0, http2=True)
    self._owns_client = http_client is None

  def close(self) -> None:
    if self._owns_client:
      self._client.close()

  def authorization_url(self, redirect_uri: str, state: str) -> str:
    """Builds a browser authorization URL for the code flow."""
    if not self.config.client_id:
      raise ToolError("YAHOO_ADS_CLIENT_ID is required.")

    params = {
      "response_type": "code",
      "client_id": self.config.client_id,
      "redirect_uri": redirect_uri,
      "scope": "yahooads",
      "state": state,
    }
    return f"{self.config.auth_base_url}/v1/authorize?{urlencode(params)}"

  def exchange_authorization_code(
    self, *, code: str, redirect_uri: str
  ) -> dict[str, Any]:
    """Exchanges an authorization code for access and refresh tokens."""
    self._require_client_credentials()
    return self._request_token(
      {
        "grant_type": "authorization_code",
        "client_id": self.config.client_id,
        "client_secret": self.config.client_secret,
        "redirect_uri": redirect_uri,
        "code": code,
      }
    )

  def refresh_access_token(self, refresh_token: str | None = None) -> dict[str, Any]:
    """Gets a new access token from a refresh token."""
    self._require_client_credentials()
    token = refresh_token or self.config.refresh_token
    if not token:
      raise ToolError("YAHOO_ADS_REFRESH_TOKEN is required.")

    return self._request_token(
      {
        "grant_type": "refresh_token",
        "client_id": self.config.client_id,
        "client_secret": self.config.client_secret,
        "refresh_token": token,
      }
    )

  def request(
    self,
    *,
    api: ApiType,
    service: str,
    method: str,
    payload: Mapping[str, Any] | None = None,
    base_account_id: str | int | None = None,
    access_token: str | None = None,
  ) -> dict[str, Any] | list[Any] | str | None:
    """Calls a Yahoo Ads service method."""
    token = access_token or self.config.access_token
    if not token:
      token = self.refresh_access_token()["access_token"]

    headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json",
    }
    resolved_base_account_id = base_account_id or self.config.base_account_id
    if resolved_base_account_id:
      headers["x-z-base-account-id"] = str(resolved_base_account_id)

    url = self._service_url(api=api, service=service, method=method)
    response = self._client.post(url, json=dict(payload or {}), headers=headers)
    return self._parse_response(response)

  def _request_token(self, data: Mapping[str, Any]) -> dict[str, Any]:
    response = self._client.post(
      f"{self.config.auth_base_url}/v1/token",
      data=data,
      headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    parsed = self._parse_response(response)
    if not isinstance(parsed, dict):
      raise ToolError("Unexpected OAuth token response.")
    return parsed

  def _service_url(self, *, api: ApiType, service: str, method: str) -> str:
    if api == "search":
      base = self.config.search_base_url
    elif api == "display":
      base = self.config.display_base_url
    else:
      raise ToolError("api must be 'search' or 'display'.")

    version = self.config.api_version.strip("/")
    return f"{base.rstrip('/')}/{version}/{service}/{method}"

  def _require_client_credentials(self) -> None:
    if not self.config.client_id:
      raise ToolError("YAHOO_ADS_CLIENT_ID is required.")
    if not self.config.client_secret:
      raise ToolError("YAHOO_ADS_CLIENT_SECRET is required.")

  @staticmethod
  def _parse_response(
    response: httpx.Response,
  ) -> dict[str, Any] | list[Any] | str | None:
    try:
      response.raise_for_status()
    except httpx.HTTPStatusError as exc:
      detail = _error_detail(exc.response)
      raise ToolError(detail) from exc

    if not response.content:
      return None

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
      return response.json()
    return response.text


def _error_detail(response: httpx.Response) -> str:
  try:
    body = response.json()
  except ValueError:
    body = response.text
  return f"Yahoo Ads API request failed: HTTP {response.status_code}: {body}"
