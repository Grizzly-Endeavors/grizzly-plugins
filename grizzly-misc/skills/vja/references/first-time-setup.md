# vja first-time setup

Start where the symptom points:

- `vja: command not found` → steps 1 to 5.
- `vja user show < /dev/null` prints `Username: Aborted!` → step 3, then step 5.

Step 3 needs Bear: the token is a credential only Bear can create, saved from Bear's own terminal. Run the other steps yourself.

## 1. Install

Check the prerequisites:

```bash
pipx --version; python3 --version; jq --version
```

- pipx or jq missing → `sudo -n apt install -y pipx jq`. If sudo says a password is required, ask Bear to run `sudo apt install pipx jq`.
- Python below 3.12 → stop and tell Bear; vja needs 3.12 or newer.

Pick the version:

```bash
curl -s https://pypi.org/pypi/vja/json | jq -r .info.version              # newest vja
curl -s https://todo.grizzly-endeavors.com/api/v1/info | jq -r .version   # server, e.g. v2.6.0
```

Read https://gitlab.com/ce72/vja/-/raw/main/CHANGELOG.md and choose the newest vja whose "Vikunja server with version >= X is required" minimum is at or below the server version. vja 6.x requires Vikunja 2.5 or newer; for an older server, choose the newest 5.x.

```bash
pipx install "vja==<version>"
vja --version
```

## 2. Point it at the instance

Write `~/.config/vja/config.rc`:

```ini
[application]
frontend_url=https://todo.grizzly-endeavors.com/
api_url=https://todo.grizzly-endeavors.com/api/v2
```

For vja 5.x, end `api_url` in `/api/v1` instead.

## 3. API token (Bear)

Ask Bear to:

1. In Vikunja, open Settings → API Tokens and create a token with every permission under **Labels, Projects, Tasks, Task Relations and User**.
2. Save it from their own fish terminal:

   ```fish
   read -s -P "Vikunja token: " tok; mkdir -p ~/.config/vja; printf '{"token": "%s"}\n' $tok > ~/.config/vja/token.json; chmod 600 ~/.config/vja/token.json; set -e tok
   ```

Then check `stat -c "%a" ~/.config/vja/token.json` prints `600` — check the mode only, never the contents. If the file is missing or not `600`, ask Bear to redo 3.2.

## 4. Shell completions (optional, for Bear's fish shell)

Skip this step if fish isn't installed.

```bash
mkdir -p ~/.config/fish/completions
_VJA_COMPLETE=fish_source vja > ~/.config/fish/completions/vja.fish
```

## 5. Verify

```bash
vja user show < /dev/null      # expect: User(id=..., username=..., default_project_id=...)
vja project ls < /dev/null     # expect: Bear's projects
vja label ls < /dev/null       # expect: Bear's labels, or nothing, with no error
```

| Result | Cause | Fix |
|---|---|---|
| `vja: command not found` after install | pipx's bin directory isn't on PATH | run `pipx ensurepath`, and call `~/.local/bin/vja` for the rest of this session |
| All three print `Username: Aborted!` | token missing, expired, or saved wrong | redo step 3 |
| `project ls` works but another prints `Username: Aborted!` | token lacks that permission (User for `user show`, Labels for `label ls`) | redo step 3 with every listed permission |
| Connection or 404 errors | `api_url` doesn't match the installed vja major version | fix step 2 |

## Upgrading

When vja commands that used to work start failing with API errors, compare `vja --version` against the server version (step 1). Choose a new version with step 1's rule, install it with `pipx install --force "vja==<version>"`, and rerun step 4 if completions were set up.
