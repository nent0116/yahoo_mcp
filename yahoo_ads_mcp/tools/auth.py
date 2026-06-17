"""OAuth helper tools."""

from typing import Any

from yahoo_ads_mcp.client import YahooAdsClient
from yahoo_ads_mcp.coordinator import mcp_server as mcp


@mcp.tool()
def get_oauth_authorization_url(redirect_uri: str, state: str) -> str:
  """Returns the Yahoo Ads OAuth authorization URL.

  Args:
      redirect_uri: Redirect URI registered for the Yahoo Ads application.
      state: Unique state value to protect the authorization request.
  """
  client = YahooAdsClient()
  try:
    return client.authorization_url(redirect_uri=redirect_uri, state=state)
  finally:
    client.close()


@mcp.tool()
def exchange_authorization_code(code: str, redirect_uri: str) -> dict[str, Any]:
  """Exchanges an authorization code for tokens.

  Args:
      code: Authorization code returned to the redirect URI.
      redirect_uri: Redirect URI used in the authorization request.
  """
  client = YahooAdsClient()
  try:
    return client.exchange_authorization_code(code=code, redirect_uri=redirect_uri)
  finally:
    client.close()


@mcp.tool()
def refresh_access_token(refresh_token: str | None = None) -> dict[str, Any]:
  """Gets a fresh access token.

  Args:
      refresh_token: Optional refresh token. If omitted,
        YAHOO_ADS_REFRESH_TOKEN is used.
  """
  client = YahooAdsClient()
  try:
    return client.refresh_access_token(refresh_token=refresh_token)
  finally:
    client.close()
