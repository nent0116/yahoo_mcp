"""Generic Yahoo Ads service caller."""

from typing import Any, Literal

from yahoo_ads_mcp.client import YahooAdsClient
from yahoo_ads_mcp.coordinator import mcp_server as mcp


@mcp.tool()
def call_yahoo_ads_api(
  api: Literal["search", "display"],
  service: str,
  method: str,
  payload: dict[str, Any] | None = None,
  base_account_id: str | None = None,
) -> dict[str, Any] | list[Any] | str | None:
  """Calls any Yahoo Ads API service method.

  Args:
      api: API family. Use "search" or "display".
      service: Service name such as "CampaignService".
      method: Method name such as "get", "add", "set", or "remove".
      payload: Request body following the official OpenAPI schema.
      base_account_id: Optional x-z-base-account-id header value.
  """
  client = YahooAdsClient()
  try:
    return client.request(
      api=api,
      service=service,
      method=method,
      payload=payload or {},
      base_account_id=base_account_id,
    )
  finally:
    client.close()
