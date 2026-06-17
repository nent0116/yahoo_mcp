from urllib.parse import parse_qs, urlparse

import httpx
import pytest
from fastmcp.exceptions import ToolError

from yahoo_ads_mcp.client import YahooAdsClient
from yahoo_ads_mcp.config import YahooAdsConfig


def config(**overrides):
  values = {
    "client_id": "client",
    "client_secret": "secret",
    "refresh_token": "refresh",
    "access_token": None,
    "base_account_id": "999",
    "api_version": "v19",
    "auth_base_url": "https://auth.example.test/oauth",
    "search_base_url": "https://search.example.test/api",
    "display_base_url": "https://display.example.test/api",
  }
  values.update(overrides)
  return YahooAdsConfig(**values)


def test_authorization_url_contains_required_params():
  client = YahooAdsClient(config(access_token="access"))

  url = client.authorization_url(
    redirect_uri="https://example.test/callback",
    state="state-value",
  )

  parsed = urlparse(url)
  params = parse_qs(parsed.query)
  assert parsed.scheme == "https"
  assert parsed.path == "/oauth/v1/authorize"
  assert params["response_type"] == ["code"]
  assert params["client_id"] == ["client"]
  assert params["redirect_uri"] == ["https://example.test/callback"]
  assert params["scope"] == ["yahooads"]
  assert params["state"] == ["state-value"]


def test_refresh_access_token_posts_form_data():
  requests = []

  def handler(request: httpx.Request) -> httpx.Response:
    requests.append(request)
    return httpx.Response(
      200,
      json={"access_token": "new-access", "expires_in": 3600},
      headers={"content-type": "application/json"},
    )

  transport = httpx.MockTransport(handler)
  client = YahooAdsClient(config(), http_client=httpx.Client(transport=transport))

  result = client.refresh_access_token()

  assert result["access_token"] == "new-access"
  request = requests[0]
  assert str(request.url) == "https://auth.example.test/oauth/v1/token"
  body = request.content.decode()
  assert "grant_type=refresh_token" in body
  assert "client_id=client" in body
  assert "client_secret=secret" in body
  assert "refresh_token=refresh" in body


def test_request_refreshes_token_and_calls_search_api():
  requests = []

  def handler(request: httpx.Request) -> httpx.Response:
    requests.append(request)
    if str(request.url) == "https://auth.example.test/oauth/v1/token":
      return httpx.Response(
        200,
        json={"access_token": "new-access", "expires_in": 3600},
        headers={"content-type": "application/json"},
      )
    return httpx.Response(
      200,
      json={"rval": {"totalNumEntries": 0}},
      headers={"content-type": "application/json"},
    )

  transport = httpx.MockTransport(handler)
  client = YahooAdsClient(config(), http_client=httpx.Client(transport=transport))

  result = client.request(
    api="search",
    service="CampaignService",
    method="get",
    payload={"accountId": 123},
  )

  assert result == {"rval": {"totalNumEntries": 0}}
  api_request = requests[1]
  assert str(api_request.url) == (
    "https://search.example.test/api/v19/CampaignService/get"
  )
  assert api_request.headers["authorization"] == "Bearer new-access"
  assert api_request.headers["x-z-base-account-id"] == "999"
  assert api_request.read() == b'{"accountId":123}'


def test_request_raises_tool_error_for_http_errors():
  transport = httpx.MockTransport(
    lambda _request: httpx.Response(
      403,
      json={"errors": [{"message": "Permission denied."}]},
      headers={"content-type": "application/json"},
    )
  )
  client = YahooAdsClient(
    config(access_token="access"),
    http_client=httpx.Client(transport=transport),
  )

  with pytest.raises(ToolError, match="HTTP 403"):
    client.request(
      api="display",
      service="CampaignService",
      method="get",
      payload={"accountId": 123},
    )
