# Workbench — First-Time Setup

Read this when `~/workbench/` does not exist yet. Complete these steps in order, then return to tool authoring.

## 1. Run the setup script

Run `assets/setup.sh` from the directory containing this `SETUP.md` (`<skill-dir>`):

```bash
bash <skill-dir>/assets/setup.sh
```

This creates `~/workbench/tools/` and `~/workbench/logs/`, copies `server.py` and `home.html` to `~/workbench/`, copies `welcome.html` to `~/workbench/tools/`, and on macOS interactively offers `launchd` auto-start.

## 2. Start the server (auto-start on login)

### Linux (`systemd --user`)

Create `~/.config/systemd/user/workbench.service`:

```ini
[Unit]
Description=Personal Workbench HTTP Server

[Service]
ExecStart=/usr/bin/python3 %h/workbench/server.py
WorkingDirectory=%h/workbench
Environment=WORKBENCH_HOST=127.0.0.1
Environment=WORKBENCH_PORT=8765
Restart=on-failure

[Install]
WantedBy=default.target
```

Then enable and start it:

```bash
systemctl --user daemon-reload
systemctl --user enable --now workbench.service
```

### macOS (`launchd`)

If `setup.sh` did not already set it up, write `~/Library/LaunchAgents/com.workbench.plist` pointing `/usr/bin/python3` at `$HOME/workbench/server.py` with `WORKBENCH_HOST=127.0.0.1` and `WORKBENCH_PORT=8765`, then run `launchctl load` and `launchctl start com.workbench`.

### Ad-hoc / foreground

```bash
python3 ~/workbench/server.py
```

## 3. Verify

Confirm `http://localhost:8765` responds (e.g. `curl -sf http://127.0.0.1:8765/ >/dev/null`), tell the user the workbench is ready, and continue with the requested tool.
