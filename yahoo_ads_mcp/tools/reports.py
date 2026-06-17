"""ReportDefinitionService tools."""

from typing import Any, Literal

from fastmcp.exceptions import ToolError

from yahoo_ads_mcp.client import YahooAdsClient
from yahoo_ads_mcp.coordinator import mcp_server as mcp


@mcp.tool()
def get_report_definitions(
  account_id: int,
  api: Literal["search", "display"] = "search",
  report_job_ids: list[int] | None = None,
  report_types: list[str] | None = None,
  base_account_id: str | None = None,
  start_index: int = 1,
  number_results: int = 100,
) -> dict[str, Any] | list[Any] | str | None:
  """Gets report definitions and job status."""
  payload: dict[str, Any] = {
    "accountId": account_id,
    "startIndex": start_index,
    "numberResults": number_results,
  }
  if report_job_ids:
    payload["reportJobIds"] = report_job_ids
  if report_types:
    if api == "display":
      raise ToolError("report_types is only supported for Search Ads reports.")
    payload["reportTypes"] = report_types
  return _call_report(
    api=api, method="get", payload=payload, base_account_id=base_account_id
  )


@mcp.tool()
def add_report_definition(
  account_id: int,
  report_name: str,
  report_type: str,
  fields: list[str],
  report_date_range_type: str,
  api: Literal["search", "display"] = "search",
  base_account_id: str | None = None,
  date_range: dict[str, str] | None = None,
  report_language: str | None = None,
  report_compress_type: str | None = None,
  report_download_encode: str | None = None,
) -> dict[str, Any] | list[Any] | str | None:
  """Creates a report definition.

  The generated report can be polled with get_report_definitions.
  """
  report_definition: dict[str, Any] = {
    "accountId": account_id,
    "reportName": report_name,
    "fields": fields,
    "reportDateRangeType": report_date_range_type,
  }
  if api == "search":
    report_definition["reportType"] = report_type
  else:
    report_definition["reportTypeCondition"] = {"reportType": report_type}
  if date_range:
    report_definition["dateRange"] = date_range
  if report_language:
    report_definition["reportLanguage"] = report_language
  if report_compress_type:
    report_definition["reportCompressType"] = report_compress_type
  if report_download_encode:
    report_definition["reportDownloadEncode"] = report_download_encode

  payload = {
    "accountId": account_id,
    "operand": [report_definition],
  }
  return _call_report(
    api=api, method="add", payload=payload, base_account_id=base_account_id
  )


@mcp.tool()
def remove_report_definition(
  account_id: int,
  report_job_ids: list[int],
  api: Literal["search", "display"] = "search",
  base_account_id: str | None = None,
) -> dict[str, Any] | list[Any] | str | None:
  """Removes report definitions."""
  payload = {
    "accountId": account_id,
    "operand": [
      {"accountId": account_id, "reportJobId": report_job_id}
      for report_job_id in report_job_ids
    ],
  }
  return _call_report(
    api=api, method="remove", payload=payload, base_account_id=base_account_id
  )


@mcp.tool()
def get_report_fields(
  report_type: str,
  api: Literal["search", "display"] = "search",
  lang: Literal["EN", "JA"] = "EN",
  base_account_id: str | None = None,
) -> dict[str, Any] | list[Any] | str | None:
  """Gets available fields for a report type."""
  payload = {"reportType": report_type}
  if api == "display":
    payload["lang"] = lang
  return _call_report(
    api=api,
    method="getReportFields",
    payload=payload,
    base_account_id=base_account_id,
  )


def _call_report(
  *,
  api: Literal["search", "display"],
  method: str,
  payload: dict[str, Any],
  base_account_id: str | None,
) -> dict[str, Any] | list[Any] | str | None:
  client = YahooAdsClient()
  try:
    return client.request(
      api=api,
      service="ReportDefinitionService",
      method=method,
      payload=payload,
      base_account_id=base_account_id,
    )
  finally:
    client.close()
