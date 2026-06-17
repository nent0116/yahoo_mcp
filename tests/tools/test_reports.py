from unittest import mock

import pytest
from fastmcp.exceptions import ToolError

from yahoo_ads_mcp.tools import reports


def test_add_report_definition_uses_search_report_type():
  client = mock.Mock()
  client.request.return_value = {"ok": True}

  with mock.patch("yahoo_ads_mcp.tools.reports.YahooAdsClient", return_value=client):
    result = reports.add_report_definition(
      account_id=123,
      report_name="campaign-report",
      report_type="CAMPAIGN",
      fields=["CAMPAIGN_ID", "IMPS"],
      report_date_range_type="YESTERDAY",
      api="search",
      date_range={"startDate": "20260616", "endDate": "20260616"},
    )

  assert result == {"ok": True}
  client.request.assert_called_once_with(
    api="search",
    service="ReportDefinitionService",
    method="add",
    payload={
      "accountId": 123,
      "operand": [
        {
          "accountId": 123,
          "reportName": "campaign-report",
          "reportType": "CAMPAIGN",
          "fields": ["CAMPAIGN_ID", "IMPS"],
          "reportDateRangeType": "YESTERDAY",
          "dateRange": {"startDate": "20260616", "endDate": "20260616"},
        }
      ],
    },
    base_account_id=None,
  )
  client.close.assert_called_once()


def test_add_report_definition_uses_display_report_type_condition():
  client = mock.Mock()
  client.request.return_value = {"ok": True}

  with mock.patch("yahoo_ads_mcp.tools.reports.YahooAdsClient", return_value=client):
    reports.add_report_definition(
      account_id=123,
      report_name="ad-report",
      report_type="AD",
      fields=["AD_ID", "IMPS"],
      report_date_range_type="YESTERDAY",
      api="display",
      base_account_id="999",
    )

  _, kwargs = client.request.call_args
  operand = kwargs["payload"]["operand"][0]
  assert operand["reportTypeCondition"] == {"reportType": "AD"}
  assert "reportType" not in operand
  assert kwargs["base_account_id"] == "999"


def test_get_report_fields_adds_lang_for_display_only():
  client = mock.Mock()
  client.request.return_value = {"ok": True}

  with mock.patch("yahoo_ads_mcp.tools.reports.YahooAdsClient", return_value=client):
    reports.get_report_fields(report_type="AD", api="display", lang="JA")

  _, kwargs = client.request.call_args
  assert kwargs["payload"] == {"reportType": "AD", "lang": "JA"}


def test_get_report_definitions_sends_report_types_for_search():
  client = mock.Mock()
  client.request.return_value = {"ok": True}

  with mock.patch("yahoo_ads_mcp.tools.reports.YahooAdsClient", return_value=client):
    reports.get_report_definitions(
      account_id=123,
      api="search",
      report_types=["CAMPAIGN"],
    )

  _, kwargs = client.request.call_args
  assert kwargs["payload"]["reportTypes"] == ["CAMPAIGN"]
  client.close.assert_called_once()


def test_get_report_definitions_rejects_report_types_for_display():
  with pytest.raises(ToolError, match="only supported for Search Ads"):
    reports.get_report_definitions(
      account_id=123,
      api="display",
      report_types=["AD"],
    )
