from unittest import mock

import pytest
from fastmcp.exceptions import ToolError

from yahoo_ads_mcp.tools import generic


def test_call_yahoo_ads_api_allows_get_methods():
  client = mock.Mock()
  client.request.return_value = {"ok": True}

  with mock.patch("yahoo_ads_mcp.tools.generic.YahooAdsClient", return_value=client):
    result = generic.call_yahoo_ads_api(
      api="search",
      service="CampaignService",
      method="get",
      payload={"accountId": 123},
      base_account_id="999",
    )

  assert result == {"ok": True}
  client.request.assert_called_once_with(
    api="search",
    service="CampaignService",
    method="get",
    payload={"accountId": 123},
    base_account_id="999",
  )
  client.close.assert_called_once()


def test_call_yahoo_ads_api_rejects_write_methods():
  client = mock.Mock()
  client.request.side_effect = ToolError(
    "Only get/download methods and ReportDefinitionService add/remove are allowed"
  )

  with (
    mock.patch("yahoo_ads_mcp.tools.generic.YahooAdsClient", return_value=client),
    pytest.raises(ToolError, match="Only get/download methods"),
  ):
    generic.call_yahoo_ads_api(
      api="search",
      service="CampaignService",
      method="remove",
      payload={"accountId": 123},
    )

  client.close.assert_called_once()
