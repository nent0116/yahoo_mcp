"""Configuration for Yahoo Ads MCP."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_API_VERSION = "v19"
DEFAULT_AUTH_BASE_URL = "https://biz-oauth.yahoo.co.jp/oauth"
DEFAULT_SEARCH_BASE_URL = "https://ads-search.yahooapis.jp/api"
DEFAULT_DISPLAY_BASE_URL = "https://ads-display.yahooapis.jp/api"
DEFAULT_CONFIG_PATH = "~/yahoo-ads.yaml"


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
    yaml_config = _load_yaml_config()

    return cls(
      client_id=_env_or_yaml("YAHOO_ADS_CLIENT_ID", yaml_config, "client_id"),
      client_secret=_env_or_yaml(
        "YAHOO_ADS_CLIENT_SECRET", yaml_config, "client_secret"
      ),
      refresh_token=_env_or_yaml(
        "YAHOO_ADS_REFRESH_TOKEN", yaml_config, "refresh_token"
      ),
      access_token=_env_or_yaml("YAHOO_ADS_ACCESS_TOKEN", yaml_config, "access_token"),
      base_account_id=_env_or_yaml(
        "YAHOO_ADS_BASE_ACCOUNT_ID", yaml_config, "base_account_id"
      ),
      api_version=_env_or_yaml(
        "YAHOO_ADS_API_VERSION",
        yaml_config,
        "api_version",
        default=DEFAULT_API_VERSION,
      ),
      auth_base_url=_env_or_yaml(
        "YAHOO_ADS_AUTH_BASE_URL",
        yaml_config,
        "auth_base_url",
        default=DEFAULT_AUTH_BASE_URL,
      ),
      search_base_url=_env_or_yaml(
        "YAHOO_ADS_SEARCH_BASE_URL",
        yaml_config,
        "search_base_url",
        default=DEFAULT_SEARCH_BASE_URL,
      ),
      display_base_url=_env_or_yaml(
        "YAHOO_ADS_DISPLAY_BASE_URL",
        yaml_config,
        "display_base_url",
        default=DEFAULT_DISPLAY_BASE_URL,
      ),
    )


def _load_yaml_config() -> dict[str, str | None]:
  config_path = Path(
    os.getenv("YAHOO_ADS_CONFIG_PATH") or DEFAULT_CONFIG_PATH
  ).expanduser()
  if not config_path.is_file():
    return {}

  with config_path.open(encoding="utf-8") as config_file:
    data = yaml.safe_load(config_file) or {}

  if not isinstance(data, dict):
    raise ValueError(f"Yahoo Ads config must be a YAML mapping: {config_path}")

  section = data.get("yahoo_ads") or data.get("env") or data
  if not isinstance(section, dict):
    raise ValueError(f"Yahoo Ads config section must be a YAML mapping: {config_path}")

  allow_short_keys = section is not data or not _looks_like_google_ads_config(data)

  return {
    "client_id": _yaml_value(
      section,
      "YAHOO_ADS_CLIENT_ID",
      *(_short_keys("client_id", allow=allow_short_keys)),
    ),
    "client_secret": _yaml_value(
      section,
      "YAHOO_ADS_CLIENT_SECRET",
      *(_short_keys("client_secret", allow=allow_short_keys)),
    ),
    "refresh_token": _yaml_value(
      section,
      "YAHOO_ADS_REFRESH_TOKEN",
      *(_short_keys("refresh_token", allow=allow_short_keys)),
    ),
    "access_token": _yaml_value(
      section,
      "YAHOO_ADS_ACCESS_TOKEN",
      *(_short_keys("access_token", allow=allow_short_keys)),
    ),
    "base_account_id": _yaml_value(
      section,
      "YAHOO_ADS_BASE_ACCOUNT_ID",
      *(
        _short_keys(
          "base_account_id",
          "baseAccountId",
          "base_account",
          allow=allow_short_keys,
        )
      ),
    ),
    "api_version": _yaml_value(
      section,
      "YAHOO_ADS_API_VERSION",
      *(_short_keys("api_version", allow=allow_short_keys)),
    ),
    "auth_base_url": _yaml_value(
      section,
      "YAHOO_ADS_AUTH_BASE_URL",
      *(_short_keys("auth_base_url", allow=allow_short_keys)),
    ),
    "search_base_url": _yaml_value(
      section,
      "YAHOO_ADS_SEARCH_BASE_URL",
      *(_short_keys("search_base_url", allow=allow_short_keys)),
    ),
    "display_base_url": _yaml_value(
      section,
      "YAHOO_ADS_DISPLAY_BASE_URL",
      *(_short_keys("display_base_url", allow=allow_short_keys)),
    ),
  }


def _looks_like_google_ads_config(data: dict[str, Any]) -> bool:
  return any(key in data for key in ("developer_token", "login_customer_id"))


def _short_keys(*keys: str, allow: bool) -> tuple[str, ...]:
  return keys if allow else ()


def _yaml_value(config: dict[str, Any], *keys: str) -> str | None:
  for key in keys:
    value = config.get(key)
    if value not in (None, ""):
      return str(value)
  return None


def _env_or_yaml(
  env_name: str,
  yaml_config: dict[str, str | None],
  yaml_key: str,
  *,
  default: str | None = None,
) -> str | None:
  return (
    os.getenv(env_name)
    or yaml_config.get(yaml_key)
    or default
  )


def get_config() -> YahooAdsConfig:
  """Returns the current configuration."""
  return YahooAdsConfig.from_env()
