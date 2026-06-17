"""Configuration for Yahoo Ads MCP."""

import os
from dataclasses import dataclass

DEFAULT_API_VERSION = "v19"
DEFAULT_AUTH_BASE_URL = "https://biz-oauth.yahoo.co.jp/oauth"
DEFAULT_SEARCH_BASE_URL = "https://ads-search.yahooapis.jp/api"
DEFAULT_DISPLAY_BASE_URL = "https://ads-display.yahooapis.jp/api"


@dataclass(frozen=True)
class YahooAdsConfig:
  """Runtime configuration loaded from environment variables."""

  client_id: str | None
  client_secret: str | None
  refresh_token: str | None
  access_token: str | None
  base_account_id: str | None
  api_version: str
  auth_base_url: str
  search_base_url: str
  display_base_url: str

  @classmethod
  def from_env(cls) -> "YahooAdsConfig":
    return cls(
      client_id=os.getenv("YAHOO_ADS_CLIENT_ID"),
      client_secret=os.getenv("YAHOO_ADS_CLIENT_SECRET"),
      refresh_token=os.getenv("YAHOO_ADS_REFRESH_TOKEN"),
      access_token=os.getenv("YAHOO_ADS_ACCESS_TOKEN"),
      base_account_id=os.getenv("YAHOO_ADS_BASE_ACCOUNT_ID"),
      api_version=os.getenv("YAHOO_ADS_API_VERSION", DEFAULT_API_VERSION),
      auth_base_url=os.getenv("YAHOO_ADS_AUTH_BASE_URL", DEFAULT_AUTH_BASE_URL),
      search_base_url=os.getenv("YAHOO_ADS_SEARCH_BASE_URL", DEFAULT_SEARCH_BASE_URL),
      display_base_url=os.getenv(
        "YAHOO_ADS_DISPLAY_BASE_URL", DEFAULT_DISPLAY_BASE_URL
      ),
    )


def get_config() -> YahooAdsConfig:
  """Returns the current configuration."""
  return YahooAdsConfig.from_env()
