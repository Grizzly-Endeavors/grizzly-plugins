# Delegate — Running Tasks with Jules

## CLI Quick Reference

```
jules remote new --repo <owner/repo> --session "<prompt>"   # task on a specific repo
jules remote new --session "<prompt>"                        # infer repo from CWD
jules remote new --session "<prompt>" --parallel 3           # 3 parallel attempts (max 5)
jules remote list --repo                                     # list connected repos
jules remote list --session                                  # list all sessions
jules remote pull --session <id>                             # pull completed changes locally
jules                                                        # launch TUI dashboard
```

Jules accepts piped stdin as the session prompt. `--repo .` and omitting
`--repo` both infer from the current git remote.

## Single Task

Translate what the user wants into a concrete prompt and run it:

```bash
jules remote new --session "Write unit tests for src/services/payment/ using Jest. Cover checkout, refunds, and edge cases like expired cards. Mock Stripe API calls."
```

If the user is vague ("fix the login page"), sharpen it before sending:

**User says:** "The login page is broken on mobile"
**You send:** `jules remote new --session "Fix responsive layout in src/pages/Login.tsx. Ensure the page renders correctly under 768px. Check for overflow on form inputs and submit button."`

**User says:** "Bump React to v19"
**You send:** `jules remote new --session "Upgrade React from v18 to v19. Update deprecated API usage per the React 19 migration guide. Fix resulting TypeScript errors. Run existing tests and fix failures."`

Use `--parallel` when the task is ambiguous or creative and multiple approaches
would be useful.

## Batch — TODO Files

Each line becomes a session:

```bash
grep -v '^\s*$' TODO.md | grep -v '^\s*#' | while IFS= read -r line; do
  jules remote new --repo . --session "$line"
done
```

If the TODO lines are rough notes, rewrite each into a proper Jules prompt
before dispatching. A line like "fix the date picker" should become "Fix the
DatePicker component in src/components/DatePicker.tsx — it does not handle
timezone offsets correctly. Use dayjs for timezone-aware formatting."

## Batch — GitHub Issues

Send the top assigned issue:

```bash
gh issue list --assignee @me --limit 1 --json title \
  | jq -r '.[0].title' \
  | jules remote new --repo .
```

Fan out all assigned issues:

```bash
gh issue list --assignee @me --json title,number \
  | jq -r '.[] | "Fix issue #\(.number): \(.title)"' \
  | while IFS= read -r line; do
    jules remote new --repo . --session "$line"
  done
```

Filter by label:

```bash
gh issue list --label "good-first-issue" --json title,number \
  | jq -r '.[] | "Fix issue #\(.number): \(.title)"' \
  | while IFS= read -r line; do
    jules remote new --repo . --session "$line"
  done
```

Use Gemini CLI to triage:

```bash
gemini -p "find the most tedious issue, print it verbatim\n$(gh issue list --assignee @me)" \
  | jules remote new --repo .
```

## Batch — Multi-Repo

Same change across repos:

```bash
repos=("myorg/frontend" "myorg/backend" "myorg/shared-lib")
for repo in "${repos[@]}"; do
  jules remote new --repo "$repo" --session "Bump eslint to v9 and fix all new lint errors"
done
```

## Batch — CSV

```bash
while IFS=, read -r repo task; do
  jules remote new --repo "$repo" --session "$task"
done < tasks.csv
```

## Checking Status and Pulling Results

```bash
jules remote list --session           # see all sessions
jules remote pull --session <id>      # pull changes locally
jules                                 # TUI dashboard
```

Via API:

```bash
# Get session status
curl -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID"

# Get activity log
curl -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities"
```

## Follow-Up Messages

If Jules gets stuck or asks a question:

```bash
curl -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Use the existing auth middleware, do not create a new one"}' \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:sendMessage"
```

Or use the TUI to respond interactively.

## Rate Limits

- **Free:** 15 tasks/day, 3 concurrent
- **Pro ($19.99/mo):** ~100 tasks/day, ~15 concurrent
- **Ultra ($124.99/mo):** ~300 tasks/day, ~60 concurrent

When scripting batches, add a small delay between requests.
