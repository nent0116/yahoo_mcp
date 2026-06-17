"""FastMCP coordinator for LY/Yahoo! JAPAN Ads API."""

from fastmcp import FastMCP

mcp_server = FastMCP(
  name="Yahoo Ads API",
  mask_error_details=True,
  client_log_level="error",
)
