"""stdio entry point for LY/Yahoo! JAPAN Ads API MCP."""

import dotenv

from yahoo_ads_mcp import server  # Registers tool modules.
from yahoo_ads_mcp.coordinator import mcp_server

dotenv.load_dotenv()


def main() -> None:
  """Runs the MCP server with stdio transport."""
  _ = server.tools
  mcp_server.run(
    transport="stdio",
    show_banner=False,
  )


if __name__ == "__main__":
  main()
