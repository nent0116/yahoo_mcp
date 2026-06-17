"""MCP server entry point for LY/Yahoo! JAPAN Ads API."""

import dotenv

from yahoo_ads_mcp.coordinator import mcp_server
from yahoo_ads_mcp.tools import accounts, auth, campaigns, generic, reports

dotenv.load_dotenv()

tools = [auth, accounts, generic, campaigns, reports]


def main() -> None:
  """Runs the MCP server with streamable HTTP transport."""
  print("Yahoo Ads MCP server starting...")
  mcp_server.run(
    transport="streamable-http",
    show_banner=False,
  )


if __name__ == "__main__":
  main()
