"""Campaign and ad entity read tools."""

from typing import Any, Literal

from yahoo_ads_mcp.client import YahooAdsClient
from yahoo_ads_mcp.coordinator import mcp_server as mcp


@mcp.tool()
def get_campaigns(
  account_id: int,
  api: Literal["search", "display"] = "search",
  campaign_ids: list[int] | None = None,
  user_statuses: list[str] | None = None,
  base_account_id: str | None = None,
  start_index: int = 1,
  number_results: int = 500,
) -> dict[str, Any] | list[Any] | str | None:
  """Gets campaigns."""
  payload: dict[str, Any] = {
    "accountId": account_id,
    "startIndex": start_index,
    "numberResults": number_results,
  }
  if campaign_ids:
    payload["campaignIds"] = campaign_ids
  if user_statuses:
    payload["userStatuses"] = user_statuses
  return _get(
    api=api,
    service="CampaignService",
    payload=payload,
    base_account_id=base_account_id,
  )


@mcp.tool()
def get_ad_groups(
  account_id: int,
  api: Literal["search", "display"] = "search",
  campaign_ids: list[int] | None = None,
  ad_group_ids: list[int] | None = None,
  user_statuses: list[str] | None = None,
  base_account_id: str | None = None,
  start_index: int = 1,
  number_results: int = 500,
) -> dict[str, Any] | list[Any] | str | None:
  """Gets ad groups."""
  payload: dict[str, Any] = {
    "accountId": account_id,
    "startIndex": start_index,
    "numberResults": number_results,
  }
  if campaign_ids:
    payload["campaignIds"] = campaign_ids
  if ad_group_ids:
    payload["adGroupIds"] = ad_group_ids
  if user_statuses:
    payload["userStatuses"] = user_statuses
  return _get(
    api=api,
    service="AdGroupService",
    payload=payload,
    base_account_id=base_account_id,
  )


@mcp.tool()
def get_ads(
  account_id: int,
  api: Literal["search", "display"] = "search",
  campaign_ids: list[int] | None = None,
  ad_group_ids: list[int] | None = None,
  ad_ids: list[int] | None = None,
  user_statuses: list[str] | None = None,
  base_account_id: str | None = None,
  start_index: int = 1,
  number_results: int = 500,
) -> dict[str, Any] | list[Any] | str | None:
  """Gets ads."""
  payload: dict[str, Any] = {
    "accountId": account_id,
    "startIndex": start_index,
    "numberResults": number_results,
  }
  if campaign_ids:
    payload["campaignIds"] = campaign_ids
  if ad_group_ids:
    payload["adGroupIds"] = ad_group_ids
  if ad_ids:
    # Search Ads and Display Ads use the same selector key for ad IDs in v19.
    payload["adIds"] = ad_ids
  if user_statuses:
    payload["userStatuses"] = user_statuses
  return _get(
    api=api,
    service="AdGroupAdService",
    payload=payload,
    base_account_id=base_account_id,
  )


def _get(
  *,
  api: Literal["search", "display"],
  service: str,
  payload: dict[str, Any],
  base_account_id: str | None,
) -> dict[str, Any] | list[Any] | str | None:
  client = YahooAdsClient()
  try:
    return client.request(
      api=api,
      service=service,
      method="get",
      payload=payload,
      base_account_id=base_account_id,
    )
  finally:
    client.close()
