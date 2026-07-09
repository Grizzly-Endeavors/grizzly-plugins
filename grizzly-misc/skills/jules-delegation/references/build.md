# Build — Creating Automation Around Jules

When the user wants to build something that triggers Jules programmatically,
use the REST API. The CLI is for terminal use; the API is for machines.

## API Quick Reference

Base URL: `https://jules.googleapis.com/v1alpha`
Auth header: `x-goog-api-key: $JULES_API_KEY`

| Endpoint | Method | Purpose |
|---|---|---|
| `/sources` | GET | List connected repos |
| `/sources/{source}` | GET | Repo details + branches |
| `/sessions` | POST | Create session |
| `/sessions` | GET | List sessions |
| `/sessions/{id}` | GET | Get session details |
| `/sessions/{id}:sendMessage` | POST | Send follow-up message |
| `/sessions/{id}:approvePlan` | POST | Approve pending plan |
| `/sessions/{id}/activities` | GET | Session events/progress |

### Create Session Payload

```json
{
  "prompt": "task description",
  "title": "optional title",
  "sourceContext": {
    "source": "sources/github-owner-repo",
    "githubRepoContext": {
      "startingBranch": "main"
    }
  },
  "automationMode": "AUTO_CREATE_PR",
  "requirePlanApproval": false
}
```

- `automationMode: "AUTO_CREATE_PR"` — Jules opens a PR on completion.
- `requirePlanApproval: true` — Jules pauses after planning, waits for
  approval via the approvePlan endpoint.
- Omit `sourceContext` for repoless sessions (ephemeral cloud env with Node,
  Python, Rust, Bun preloaded).

### Session States

`ACTIVE`, `COMPLETED`, `FAILED`

### Source Name Discovery

Source names follow the pattern `sources/github-{owner}-{repo}` but can vary.
Always discover them first:

```bash
curl -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources"
```

---

## GitHub Actions Patterns

### Issue-Triggered — Auto-Assign to Jules

```yaml
name: Assign labeled issues to Jules
on:
  issues:
    types: [opened]

jobs:
  delegate:
    if: contains(github.event.issue.labels.*.name, 'jules')
    runs-on: ubuntu-latest
    steps:
      - name: Send to Jules
        env:
          JULES_API_KEY: ${{ secrets.JULES_API_KEY }}
        run: |
          SOURCE="sources/github-${{ github.repository_owner }}-${{ github.event.repository.name }}"
          curl -s -X POST \
            -H "x-goog-api-key: $JULES_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$(jq -n \
              --arg prompt "Fix issue #${{ github.event.issue.number }}: ${{ github.event.issue.title }}" \
              --arg title "Issue #${{ github.event.issue.number }}" \
              --arg source "$SOURCE" \
              '{prompt: $prompt, title: $title, sourceContext: {source: $source, githubRepoContext: {startingBranch: "main"}}, automationMode: "AUTO_CREATE_PR"}')" \
            "https://jules.googleapis.com/v1alpha/sessions"
```

The `if` condition gates on the "jules" label — only tagged issues get sent.

### Post-Merge Follow-Up

```yaml
name: Post-merge Jules tasks
on:
  pull_request:
    types: [closed]

jobs:
  follow-up:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Update changelog
        env:
          JULES_API_KEY: ${{ secrets.JULES_API_KEY }}
        run: |
          SOURCE="sources/github-${{ github.repository_owner }}-${{ github.event.repository.name }}"
          curl -s -X POST \
            -H "x-goog-api-key: $JULES_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$(jq -n \
              --arg prompt "Update CHANGELOG.md for PR #${{ github.event.pull_request.number }}: ${{ github.event.pull_request.title }}. Follow Keep a Changelog format." \
              --arg source "$SOURCE" \
              '{prompt: $prompt, sourceContext: {source: $source, githubRepoContext: {startingBranch: "main"}}, automationMode: "AUTO_CREATE_PR"}')" \
            "https://jules.googleapis.com/v1alpha/sessions"
```

### Cron — Scheduled Maintenance

```yaml
name: Weekly dependency updates
on:
  schedule:
    - cron: '0 9 * * 1'

jobs:
  deps:
    runs-on: ubuntu-latest
    steps:
      - name: Bump dependencies
        env:
          JULES_API_KEY: ${{ secrets.JULES_API_KEY }}
        run: |
          curl -s -X POST \
            -H "x-goog-api-key: $JULES_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "prompt": "Check for outdated dependencies. Update all patch and minor versions. Run the test suite and fix any breakages. Do not bump major versions.",
              "title": "Weekly dep bump",
              "sourceContext": {
                "source": "sources/github-myorg-myrepo",
                "githubRepoContext": {"startingBranch": "main"}
              },
              "automationMode": "AUTO_CREATE_PR"
            }' \
            "https://jules.googleapis.com/v1alpha/sessions"
```

---

## Webhook Handlers

### Flask Example — Sentry + Slack

```python
import os, requests
from flask import Flask, request

app = Flask(__name__)
JULES_API = "https://jules.googleapis.com/v1alpha"
JULES_KEY = os.environ["JULES_API_KEY"]

def create_session(source, prompt, title=None):
    return requests.post(
        f"{JULES_API}/sessions",
        headers={
            "x-goog-api-key": JULES_KEY,
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "title": title or prompt[:80],
            "sourceContext": {
                "source": source,
                "githubRepoContext": {"startingBranch": "main"},
            },
            "automationMode": "AUTO_CREATE_PR",
        },
    )

@app.route("/webhook/sentry", methods=["POST"])
def sentry_webhook():
    data = request.json
    error_title = data.get("event", {}).get("title", "Unknown error")
    prompt = f"Investigate and fix: {error_title}. Check the stack trace, find root cause, submit a fix."
    create_session("sources/github-myorg-myapp", prompt)
    return "", 200

@app.route("/webhook/slack", methods=["POST"])
def slack_command():
    text = request.form.get("text", "")
    if not text:
        return "Usage: /jules <task description>"
    create_session("sources/github-myorg-myapp", text)
    return f"Sent to Jules: {text}"
```

---

## Common Building Blocks

### Polling for Completion

```bash
#!/bin/bash
SESSION_ID="$1"
API="https://jules.googleapis.com/v1alpha"

while true; do
  state=$(curl -s -H "x-goog-api-key: $JULES_API_KEY" \
    "$API/sessions/$SESSION_ID" | jq -r '.state')
  case "$state" in
    COMPLETED) echo "Done!"; break ;;
    FAILED)
      echo "Failed."
      curl -s -H "x-goog-api-key: $JULES_API_KEY" \
        "$API/sessions/$SESSION_ID/activities" \
        | jq '.activities[] | select(.failed != null)'
      break ;;
    *) echo "State: $state"; sleep 30 ;;
  esac
done
```

### Plan Approval Gate

For sensitive repos — Jules plans but does not execute until approved:

```bash
# Create with approval required
curl -s -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Migrate database schema from v2 to v3",
    "requirePlanApproval": true,
    "sourceContext": {
      "source": "sources/github-myorg-myapp",
      "githubRepoContext": {"startingBranch": "main"}
    }
  }' \
  "https://jules.googleapis.com/v1alpha/sessions"

# Approve after reviewing the plan in activities
curl -s -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -d '{}' \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:approvePlan"
```

### Batch via API

When you need more control than the CLI gives (specific branches, auto-PR,
plan approval):

```bash
#!/bin/bash
API="https://jules.googleapis.com/v1alpha"

while IFS=$'\t' read -r title prompt; do
  curl -s -X POST \
    -H "x-goog-api-key: $JULES_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg prompt "$prompt" \
      --arg title "$title" \
      '{prompt: $prompt, title: $title, sourceContext: {source: "sources/github-myorg-myrepo", githubRepoContext: {startingBranch: "main"}}, automationMode: "AUTO_CREATE_PR"}')" \
    "$API/sessions"
  sleep 2
done < tasks.tsv
```

### Repoless Sessions

No repo needed — Jules spins up an ephemeral environment:

```bash
curl -s -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a Python CLI that converts CSV to JSON. Include argparse, handle edge cases, add a README.",
    "title": "CSV to JSON CLI"
  }' \
  "https://jules.googleapis.com/v1alpha/sessions"
```

---

## Security Notes

- Store API keys as secrets (GitHub Actions secrets, Vault, env vars). Never
  commit them.
- Jules runs in isolated cloud VMs. It clones the repo, works there, delivers
  via PR or branch. No persistent access to local machines.
- Use `requirePlanApproval: true` for sensitive repos.
- Jules supports MCP server integrations (Linear, Render, etc) configured in
  the web UI under Settings > Integrations. Only approved MCP servers are
  allowed — Jules vets third-party integrations for security.
