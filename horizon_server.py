"""Prefect Horizon entrypoint: `horizon_server.py:mcp`.

Horizon needs a module-level FastMCP instance. The upstream package only
exposes the `build_server(config)` factory, so build the instance here from
environment variables (WEBULL_APP_KEY, WEBULL_APP_SECRET, WEBULL_ENVIRONMENT,
WEBULL_REGION_ID, WEBULL_MAX_ORDER_NOTIONAL_USD, WEBULL_MAX_ORDER_QUANTITY, ...).

Horizon runs `fastmcp inspect` on this module while building the image, and
runtime environment variables are not available at that point. Importing this
module must therefore not fail when the Webull credentials are absent. When
they are missing we fill in clearly fake placeholders so the import succeeds;
the SDK only uses credentials in the server's startup hook, so a deployment
running with placeholders fails at startup with an authentication error and
never reaches Webull with real access.
"""

import os
import sys

_PLACEHOLDER = "build-time-placeholder"

for _name in ("WEBULL_APP_KEY", "WEBULL_APP_SECRET"):
    if not os.environ.get(_name):
        os.environ[_name] = _PLACEHOLDER
        print(
            f"[horizon_server] {_name} not set; using a placeholder "
            "(expected during image build only).",
            file=sys.stderr,
        )

from webull_openapi_mcp.config import load_config, validate_config  # noqa: E402
from webull_openapi_mcp.server import build_server  # noqa: E402

config = load_config()
validate_config(config)

mcp = build_server(config)
