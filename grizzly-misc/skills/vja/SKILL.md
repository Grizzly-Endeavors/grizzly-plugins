---
name: vja
description: Manage Bear's tasks in the self-hosted Vikunja (todo.grizzly-endeavors.com) from the terminal with the vja CLI. Use when Bear asks to see what's due, list, add, edit, complete, defer, relate, or delete tasks or to-dos, to manage Vikunja projects or labels, or to list Kanban buckets. Also use when `vja` is missing or unconfigured on a machine — references/first-time-setup.md installs and configures it.
---

# vja — Vikunja tasks from the terminal

`vja` manages Bear's Vikunja at https://todo.grizzly-endeavors.com, authenticating with a personal API token in `~/.config/vja/token.json`.

## Check readiness first

Run `vja user show < /dev/null` once per session before any other vja command:

- Prints `User(id=..., ...)` → ready.
- `command not found` → do [references/first-time-setup.md](references/first-time-setup.md) from step 1.
- Prints `Username: Aborted!` → the token is missing, expired, or lacks a permission: have Bear do setup step 3, then run step 5.
- Any other error → match it against the table in setup step 5.

## Run every call with stdin closed

Put `< /dev/null` directly after the vja arguments, before any `|` — e.g. `vja ls --json < /dev/null | jq ...`. Without it, a token problem leaves vja waiting on a username prompt.

When any command prints `Username: Aborted!`, stop and tell Bear the token needs replacing (setup step 3). The instance only accepts API tokens, so ask for a new token, not a password.

## Find tasks

```bash
vja ls < /dev/null                                  # open tasks
vja ls --all < /dev/null                            # include done tasks
vja ls -o '^Home$' -l chores -p "ge 3" < /dev/null
vja ls -d "before in 7 days" < /dev/null            # due in the next 7 days, including overdue
vja ls -i dentist < /dev/null                       # title regex
vja show 12 14 < /dev/null                          # full details
```

- On `ls`, `-o` (project) and `-l` (label) are regexes: anchor with `^...$` for an exact name, since `-o Home` also matches "Homework".
- `ls -p` takes `"<op> <n>"` (`ge`, `le`, `eq`, ...); `add`/`edit -p` take a bare number.
- To read ids or fields, use JSON: `vja ls --json -i "<regex>" < /dev/null | jq '.[] | {id, title, due_date, done}'`.

## Add

```bash
vja add "Replace furnace filter" -o Home -d "friday 17:00" -p 3 -l chores -r "1h before due_date" -n "20x25x1" -v < /dev/null
```

- Quote the title as one argument.
- Pass `-o` when Bear names a project; check `vja project ls < /dev/null` when the exact name is unclear. Without `-o` the task goes to Bear's default project.
- Priority runs 1 (low) to 5 (do now).
- Dates take natural language ("tomorrow at 9", "in 3 days", "friday 17:00"). `-r` takes an absolute time or `"<duration> before due_date"`; to set the reminder at the due date, put a bare `-r` last.
- When setting `-d` or `-r`, pass `-v` and check the printed due date and reminder match what Bear asked for.
- `-l` needs an existing label; repeat `-l` for several. Check `vja label ls < /dev/null` first, and add `--force-create` only when Bear asked for a new label.
- Report the task id from `Created task <id> in project <id>` back to Bear.

## Change

```bash
vja edit 12 --done true < /dev/null                 # complete; --done false reopens
vja edit 12 14 -d monday -p 4 -v < /dev/null        # several ids at once
vja edit 12 -a "called, waiting on quote" < /dev/null   # append to the note (-n replaces it)
vja edit 12 -o Work --star < /dev/null              # move project, favorite
vja defer 12 2d -v < /dev/null                      # shift due date and reminders together (2d, 1h30m)
vja relation add 12 blocked 14 < /dev/null          # 12 is blocked by 14
```

- Complete tasks only with `vja edit <ids> --done true`. `vja done`, `toggle`, `check` and `click` flip the state, reopening tasks that are already done.
- `vja edit <id> -l <label>` and `-A <user>` toggle: each removes the label or assignee if the task already has it. Run `vja show <id> < /dev/null` first, and pass one `-l` per `edit` call.
- Pass `-v` on `edit -d`, `edit -r` and `defer`, and check the printed dates.
- Pass at least one option to `vja edit` — with none, it tries to open a browser.
- Relation kinds: subtask, parenttask, related, duplicateof, duplicates, blocking, blocked, precedes, follows, copiedfrom, copiedto.

## Delete

`vja delete <ids>` removes tasks permanently, with no confirmation prompt.

1. Skip confirmation only when Bear gave the task ids. When you looked the ids up from a title or description, show them with `vja show <ids> < /dev/null` and wait for Bear's yes.
2. Run `vja delete <ids> < /dev/null`.
3. Confirm they are gone: `vja ls --all --json < /dev/null | jq '[.[] | select(.id | IN(12, 14))] | length'` prints `0`.

## Projects, labels, buckets

```bash
vja project ls < /dev/null
vja project add Garden -o Home < /dev/null          # -o sets the parent project
vja label ls < /dev/null
vja label add errands < /dev/null
vja bucket ls -o Home < /dev/null                   # Kanban buckets of the project's first Kanban view
```
