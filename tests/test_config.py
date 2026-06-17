from yahoo_ads_mcp.config import (
  DEFAULT_API_VERSION,
  DEFAULT_AUTH_BASE_URL,
  DEFAULT_DISPLAY_BASE_URL,
  DEFAULT_SEARCH_BASE_URL,
  YahooAdsConfig,
)

CONFIG_ENV_NAMES = [
  "YAHOO_ADS_CONFIG_PATH",
  "YAHOO_ADS_CLIENT_ID",
  "YAHOO_ADS_CLIENT_SECRET",
  "YAHOO_ADS_REFRESH_TOKEN",
  "YAHOO_ADS_ACCESS_TOKEN",
  "YAHOO_ADS_BASE_ACCOUNT_ID",
  "YAHOO_ADS_API_VERSION",
  "YAHOO_ADS_AUTH_BASE_URL",
  "YAHOO_ADS_SEARCH_BASE_URL",
  "YAHOO_ADS_DISPLAY_BASE_URL",
]


def clear_config_env(monkeypatch):
  for name in CONFIG_ENV_NAMES:
    monkeypatch.delenv(name, raising=False)


def test_from_env_loads_yahoo_ads_yaml_section(tmp_path, monkeypatch):
  clear_config_env(monkeypatch)
  config_path = tmp_path / "yahoo-ads.yaml"
  config_path.write_text(
    """
yahoo_ads:
  client_id: yaml-client
  client_secret: yaml-secret
  refresh_token: yaml-refresh
  access_token: yaml-access
  base_account_id: 1234567890
  api_version: v20
  auth_base_url: https://auth.example.test/oauth
  search_base_url: https://search.example.test/api
  display_base_url: https://display.example.test/api
""",
    encoding="utf-8",
  )
  monkeypatch.setenv("YAHOO_ADS_CONFIG_PATH", str(config_path))

  config = YahooAdsConfig.from_env()

  assert config.client_id == "yaml-client"
  assert config.client_secret == "yaml-secret"
  assert config.refresh_token == "yaml-refresh"
  assert config.access_token == "yaml-access"
  assert config.base_account_id == "1234567890"
  assert config.api_version == "v20"
  assert config.auth_base_url == "https://auth.example.test/oauth"
  assert config.search_base_url == "https://search.example.test/api"
  assert config.display_base_url == "https://display.example.test/api"


def test_from_env_prefers_environment_over_yaml(tmp_path, monkeypatch):
  clear_config_env(monkeypatch)
  config_path = tmp_path / "yahoo-ads.yaml"
  config_path.write_text(
    """
yahoo_ads:
  client_id: yaml-client
  client_secret: yaml-secret
  refresh_token: yaml-refresh
""",
    encoding="utf-8",
  )
  monkeypatch.setenv("YAHOO_ADS_CONFIG_PATH", str(config_path))
  monkeypatch.setenv("YAHOO_ADS_CLIENT_ID", "env-client")

  config = YahooAdsConfig.from_env()

  assert config.client_id == "env-client"
  assert config.client_secret == "yaml-secret"
  assert config.refresh_token == "yaml-refresh"


def test_from_env_does_not_treat_google_ads_yaml_as_yahoo_config(
  tmp_path, monkeypatch
):
  clear_config_env(monkeypatch)
  config_path = tmp_path / "yahoo-ads.yaml"
  config_path.write_text(
    """
developer_token: google-developer-token
client_id: google-client
client_secret: google-secret
refresh_token: google-refresh
login_customer_id: "123"
""",
    encoding="utf-8",
  )
  monkeypatch.setenv("YAHOO_ADS_CONFIG_PATH", str(config_path))

  config = YahooAdsConfig.from_env()

  assert config.client_id is None
  assert config.client_secret is None
  assert config.refresh_token is None
  assert config.base_account_id is None
  assert config.api_version == DEFAULT_API_VERSION
  assert config.auth_base_url == DEFAULT_AUTH_BASE_URL
  assert config.search_base_url == DEFAULT_SEARCH_BASE_URL
  assert config.display_base_url == DEFAULT_DISPLAY_BASE_URL
