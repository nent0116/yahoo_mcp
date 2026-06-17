# Yahoo Ads MCP Server

LY/Yahoo! JAPAN Ads API を MCP から扱うためのサーバーです。
`google-marketing-solutions/google_ads_mcp` の構成を参考にしつつ、Yahoo広告向けに OAuth2 と REST API 呼び出しを実装しています。

> This project is not an official LY Corporation or Yahoo! JAPAN product.

## 対応範囲

- Search Ads API / Display Ads API v19
- OAuth2 refresh token から access token を取得
- BaseAccountService/get によるアクセス可能アカウント取得
- Search Ads / Display Ads の任意サービスメソッド呼び出し
- CampaignService/get, AdGroupService/get, AdGroupAdService/get のショートカット
- ReportDefinitionService の get/add/remove/getReportFields

Yahoo公式ドキュメントでは、2026-06-17 時点で v19 が最新です。

## セットアップ

```bash
uv sync
```

`.env`、環境変数、または `~/yahoo-ads.yaml` に以下を設定してください。

```bash
YAHOO_ADS_CLIENT_ID=...
YAHOO_ADS_CLIENT_SECRET=...
YAHOO_ADS_REFRESH_TOKEN=...

# 任意。未指定時は v19
YAHOO_ADS_API_VERSION=v19

# 任意。多くのサービスでは base account が必要です。
YAHOO_ADS_BASE_ACCOUNT_ID=...
```

YAML で管理する場合は、デフォルトで `~/yahoo-ads.yaml` を読みます。
別パスを使う場合は `YAHOO_ADS_CONFIG_PATH` を指定してください。
OS の環境変数が設定されている場合は YAML より優先されます。

```yaml
yahoo_ads:
  YAHOO_ADS_CLIENT_ID: "..."
  YAHOO_ADS_CLIENT_SECRET: "..."
  YAHOO_ADS_REFRESH_TOKEN: "..."

  # 任意。未指定時は v19
  YAHOO_ADS_API_VERSION: "v19"

  # 任意。多くのサービスでは base account が必要です。
  YAHOO_ADS_BASE_ACCOUNT_ID: "..."
```

### 環境変数の取得方法

LINEヤフー広告 API を利用するには、事前に API 利用申請とアプリケーション登録が必要です。
API 管理コンソールの操作には、API 管理ツールの管理者権限を持つビジネス ID が必要です。

- `YAHOO_ADS_CLIENT_ID`
  - LY Ads API Management Console でアプリケーションを追加すると発行されます。
  - 登録済みアプリケーションの一覧に `Client ID` として表示されます。

- `YAHOO_ADS_CLIENT_SECRET`
  - `YAHOO_ADS_CLIENT_ID` と同じ登録済みアプリケーションで確認します。
  - アプリケーション一覧の `View` から `Client secret` を表示できます。
  - パスワード相当の値なので、第三者に共有しないでください。

- `YAHOO_ADS_REFRESH_TOKEN`
  - OAuth2 認可コードフローで取得します。
  - まず `get_oauth_authorization_url` ツールで認可 URL を作成し、広告アカウント権限を持つビジネス ID でログインしてアプリケーションを承認します。
  - 承認後に取得した認可コードを `exchange_authorization_code` ツールへ渡すと、レスポンスに `refresh_token` が含まれます。
  - `access_token` は通常 1 時間で期限切れになりますが、`refresh_token` を設定しておけば再取得できます。

- `YAHOO_ADS_BASE_ACCOUNT_ID`
  - API リクエストヘッダー `x-z-base-account-id` に指定するアカウント ID です。
  - `list_base_accounts` ツールで、認可したビジネス ID が直接権限を持つ MCC アカウントまたは広告アカウントの一覧を取得できます。
  - 広告管理ツール上でもアカウント ID を確認できます。
  - 配下アカウントを広く扱う場合はルート MCC の ID、単一広告アカウントだけを扱う場合は対象広告アカウントの ID を指定します。

- `YAHOO_ADS_API_VERSION`
  - 任意項目です。未指定時は `v19` を使用します。

## 起動

```bash
uv run -m yahoo_ads_mcp.server
```

stdio transport で使う場合:

```bash
uv run -m yahoo_ads_mcp.stdio
```

MCP クライアント設定例:

```json
{
  "mcpServers": {
    "YahooAds": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/yahoo_mcp", "-m", "yahoo_ads_mcp.stdio"],
      "cwd": "/path/to/yahoo_mcp",
      "timeout": 30000,
      "trust": false,
      "env": {
        "YAHOO_ADS_CLIENT_ID": "CLIENT_ID",
        "YAHOO_ADS_CLIENT_SECRET": "CLIENT_SECRET",
        "YAHOO_ADS_REFRESH_TOKEN": "REFRESH_TOKEN",
        "YAHOO_ADS_BASE_ACCOUNT_ID": "BASE_ACCOUNT_ID"
      }
    }
  }
}
```

## 主なツール

- `get_oauth_authorization_url`
- `exchange_authorization_code`
- `refresh_access_token`
- `list_base_accounts`
- `call_yahoo_ads_api`
- `get_campaigns`
- `get_ad_groups`
- `get_ads`
- `get_report_definitions`
- `add_report_definition`
- `remove_report_definition`
- `get_report_fields`

## 任意サービス呼び出し例

```json
{
  "api": "search",
  "service": "CampaignService",
  "method": "get",
  "payload": {
    "accountId": 1234567890,
    "numberResults": 100,
    "startIndex": 1
  },
  "base_account_id": "1234567890"
}
```

## 参照元

- Google Ads MCP Server: https://github.com/google-marketing-solutions/google_ads_mcp
- LY Ads API Startup Guide: https://ads-developers.yahoo.co.jp/en/ads-api/startup-guide/api-call.html
- LY Ads API Before you start: https://ads-developers.yahoo.co.jp/en/ads-api/startup-guide/before_you_start.html
- LY Ads API Add Application: https://ads-developers.yahoo.co.jp/en/ads-api/startup-guide/app-registration.html
- LY Ads API OAuth2.0: https://ads-developers.yahoo.co.jp/en/ads-api/developers-guide/oauth.html
- LINEヤフー広告 アカウントIDとは: https://ads-help.yahoo-net.jp/s/article/H000044734?language=ja
- Search Ads OpenAPI: https://github.com/yahoojp-marketing/ads-search-api-documents
- Display Ads OpenAPI: https://github.com/yahoojp-marketing/ads-display-api-documents
