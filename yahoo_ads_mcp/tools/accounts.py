"""Account tools for Yahoo Ads APIs."""

from typing import Any, Literal

from yahoo_ads_mcp.client import YahooAdsClient
from yahoo_ads_mcp.coordinator import mcp_server as mcp

IncludeMccAccount = Literal[
  "ONLY_MCC",
  "ONLY_ROOT_MCC",
  "ONLY_ADS_ACCOUNT",
  "ALL",
  "UNKNOWN",
]
IncludeTestAccount = Literal[
  "ONLY_TEST",
  "EXCLUDE_TEST",
  "ALL",
  "UNKNOWN",
]


@mcp.tool()
def list_base_accounts(
  api: Literal["search", "display"] = "search",
  account_ids: list[int] | None = None,
  account_name: str | None = None,
  include_mcc_account: IncludeMccAccount | None = "ALL",
  include_test_account: IncludeTestAccount | None = "EXCLUDE_TEST",
  start_index: int = 1,
  number_results: int = 200,
) -> dict[str, Any] | list[Any] | str | None:
  """Lists accounts usable as x-z-base-account-id.

  Args:
      api: API family. Use "search" for Search Ads or "display" for Display Ads.
      account_ids: Optional account IDs to filter.
      account_name: Optional account name filter.
      include_mcc_account: Optional API enum value. Defaults to "ALL".
      include_test_account: Optional API enum value. Defaults to "EXCLUDE_TEST".
      start_index: Result start index.
      number_results: Number of results to retrieve.
  """
  payload: dict[str, Any] = {
    "startIndex": start_index,
    "numberResults": number_results,
  }
  if account_ids:
    payload["accountIds"] = account_ids
  if account_name:
    payload["accountName"] = account_name
  if include_mcc_account:
    payload["includeMccAccount"] = include_mcc_account
  if include_test_account:
    payload["includeTestAccount"] = include_test_account

  client = YahooAdsClient()
  try:
    return client.request(
      api=api,
      service="BaseAccountService",
      method="get",
      payload=payload,
    )
  finally:
    client.close()
