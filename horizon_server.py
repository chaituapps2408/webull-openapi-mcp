"""Prefect Horizon entrypoint: `horizon_server.py:mcp`.

Horizon needs a module-level FastMCP instance. The upstream package only
exposes the `build_server(config)` factory, so build the instance here from
environment variables (WEBULL_APP_KEY, WEBULL_APP_SECRET, WEBULL_ENVIRONMENT,
WEBULL_REGION_ID, WEBULL_MAX_ORDER_NOTIONAL_USD, WEBULL_MAX_ORDER_QUANTITY, ...).
"""

from webull_openapi_mcp.config import load_config, validate_config
from webull_openapi_mcp.server import build_server

config = load_config()
validate_config(config)

mcp = build_server(config)
