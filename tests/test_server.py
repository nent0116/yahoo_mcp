from unittest import mock

from yahoo_ads_mcp import server, stdio


@mock.patch("yahoo_ads_mcp.server.mcp_server")
def test_server_main_runs_streamable_http(mock_mcp_server):
  server.main()

  mock_mcp_server.run.assert_called_once_with(
    transport="streamable-http",
    show_banner=False,
  )


@mock.patch("yahoo_ads_mcp.stdio.mcp_server")
def test_stdio_main_runs_stdio(mock_mcp_server):
  stdio.main()

  mock_mcp_server.run.assert_called_once_with(
    transport="stdio",
    show_banner=False,
  )
