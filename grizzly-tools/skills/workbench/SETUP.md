# Workbench — first-time setup

Read this when `~/workbench/` doesn't exist and the user needs the workbench set up.
Complete all steps in order, then return to tool authoring.

## Steps

### 1. Run the setup script

```bash
bash ~/.claude/skills/workbench/assets/setup.sh
```

This script:
- Creates `~/workbench/tools/` and `~/workbench/logs/`
- Copies `server.py` and `home.html` to `~/workbench/`
- Copies `welcome.html` to `~/workbench/tools/`
- If run interactively on macOS, offers to set up launchd auto-start

### 2. Start the server (if launchd wasn't set up)

**Foreground:**
```bash
python3 ~/workbench/server.py
```

**Background:**
```bash
python3 ~/workbench/server.py &
```

**macOS launchd (auto-start on login) — if not already done by the script:**

Run `echo $HOME` to get the absolute home path, then write a plist to
`~/Library/LaunchAgents/com.workbench.plist` — replace `YOUR_HOME` with that path:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>            <string>com.workbench</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>YOUR_HOME/workbench/server.py</string>
  </array>
  <key>WorkingDirectory</key> <string>YOUR_HOME/workbench</string>
  <key>RunAtLoad</key>        <true/>
  <key>KeepAlive</key>        <true/>
  <key>StandardOutPath</key>  <string>YOUR_HOME/workbench/logs/workbench.out.log</string>
  <key>StandardErrorPath</key><string>YOUR_HOME/workbench/logs/workbench.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>WORKBENCH_HOST</key> <string>127.0.0.1</string>
    <key>WORKBENCH_PORT</key> <string>8765</string>
  </dict>
</dict>
</plist>
```

Then load and start it:
```bash
launchctl load ~/Library/LaunchAgents/com.workbench.plist
launchctl start com.workbench
```

### 3. Verify

Ask the user to open **http://localhost:8765** — they should see the workbench home page with
the "Welcome to workbench" tool listed.

If the page doesn't load, check `ps aux | grep server.py` and that port 8765 is free.

### 4. Tell the user

Workbench is ready. Tools go in `~/workbench/tools/`. Access at http://localhost:8765.
Now continue with whatever tool was originally requested.
