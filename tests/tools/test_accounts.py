from unittest import mock

from yahoo_ads_mcp.tools import accounts


def test_list_base_accounts_uses_v19_enum_defaults():
  client = mock.Mock()
  client.request.return_value = {"ok": True}

  with mock.patch("yahoo_ads_mcp.tools.accounts.YahooAdsClient", return_value=client):
    result = accounts.list_base_accounts()

  assert result == {"ok": True}
  client.request.assert_called_once_with(
    api="search",
    service="BaseAccountService",
    method="get",
    payload={
      "startIndex": 1,
      "numberResults": 200,
      "includeMccAccount": "ALL",
      "includeTestAccount": "EXCLUDE_TEST",
    },
  )
  client.close.assert_called_once()


def test_list_base_accounts_passes_filters():
  client = mock.Mock()
  client.request.return_value = {"ok": True}

  with mock.patch("yahoo_ads_mcp.tools.accounts.YahooAdsClient", return_value=client):
    accounts.list_base_accounts(
      api="display",
      account_ids=[123],
      account_name="account",
      include_mcc_account="ONLY_ADS_ACCOUNT",
      include_test_account="ALL",
      start_index=2,
      number_results=50,
    )

  _, kwargs = client.request.call_args
  assert kwargs["api"] == "display"
  assert kwargs["payload"] == {
    "startIndex": 2,
    "numberResults": 50,
    "accountIds": [123],
    "accountName": "account",
    "includeMccAccount": "ONLY_ADS_ACCOUNT",
    "includeTestAccount": "ALL",
  }
