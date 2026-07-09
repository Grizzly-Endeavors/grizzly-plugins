#!/usr/bin/env bash
# workbench setup
# Copies server files into ~/workbench and optionally configures launchd auto-start (macOS).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WB="$HOME/workbench"

# ── 1. directories ────────────────────────────────────────────────────────
echo "Creating ~/workbench..."
mkdir -p "$WB/tools" "$WB/logs"

# ── 2. copy server files ──────────────────────────────────────────────────
echo "Copying server files..."
cp "$SCRIPT_DIR/server.py"    "$WB/server.py"
cp "$SCRIPT_DIR/home.html"    "$WB/home.html"
cp "$SCRIPT_DIR/welcome.html" "$WB/tools/welcome.html"

echo ""
echo "  $WB/server.py"
echo "  $WB/home.html"
echo "  $WB/tools/welcome.html"

# ── 3. launchd auto-start (macOS only, interactive) ───────────────────────
if [[ "$(uname)" == "Darwin" && -t 0 ]]; then
  echo ""
  read -rp "Set up launchd auto-start on login? [y/N] " yn
  if [[ "${yn,,}" == "y" ]]; then
    PLIST="$HOME/Library/LaunchAgents/com.workbench.plist"
    cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>            <string>com.workbench</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$WB/server.py</string>
  </array>
  <key>WorkingDirectory</key> <string>$WB</string>
  <key>RunAtLoad</key>        <true/>
  <key>KeepAlive</key>        <true/>
  <key>StandardOutPath</key>  <string>$WB/logs/workbench.out.log</string>
  <key>StandardErrorPath</key><string>$WB/logs/workbench.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>WORKBENCH_HOST</key> <string>127.0.0.1</string>
    <key>WORKBENCH_PORT</key> <string>8765</string>
  </dict>
</dict>
</plist>
PLIST
    launchctl load "$PLIST"
    launchctl start com.workbench
    echo ""
    echo "launchd agent loaded — workbench starts automatically on login."
    echo "To stop:    launchctl stop com.workbench"
    echo "To disable: launchctl unload $PLIST"
  fi
fi

# ── 4. done ───────────────────────────────────────────────────────────────
echo ""
echo "Done. Open http://localhost:8765"
echo ""
if [[ "$(uname)" != "Darwin" ]] || [[ ! -f "$HOME/Library/LaunchAgents/com.workbench.plist" ]]; then
  echo "To start the server:"
  echo "  python3 $WB/server.py"
fi
