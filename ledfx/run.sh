#!/bin/sh
# Start LedFx with its configuration in the add-on's persistent /data directory.
set -eu

CONFIG_DIR=/data/ledfx
mkdir -p "$CONFIG_DIR"

VERBOSE=""
if python3 -c 'import json,sys; sys.exit(0 if json.load(open("/data/options.json")).get("verbose") else 1)' 2>/dev/null; then
    VERBOSE="-v"
fi

echo "Starting LedFx $(/app/.venv/bin/ledfx --version 2>/dev/null || true), config in $CONFIG_DIR"
# --offline: no Sentry crash reports, no update checks
exec /app/.venv/bin/ledfx -c "$CONFIG_DIR" --host 0.0.0.0 -p 8888 --offline --no-tray $VERBOSE
