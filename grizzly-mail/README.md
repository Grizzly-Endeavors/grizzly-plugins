# grizzly-mail

An MCP server giving Claude Code access to three mailboxes on the self-hosted Stalwart mail server: its own test mailbox `claude@grizzly-endeavors.com`, built for end-to-end mail testing; the company mailbox `billing@grizzly-endeavors.com` (which also receives `admin@`), for reading, filing and answering the company's bank, payment, government and vendor mail; and Goalaxi's support mailbox `support@goalaxi.com`, for triaging support mail and answering the simple requests.

## Mailboxes

Every tool takes an optional `mailbox` argument; it defaults to `claude`, so existing callers are unaffected.

| Mailbox | Login | Addresses | Deleting |
|---|---|---|---|
| `claude` | `claude@grizzly-endeavors.com` | `claude@` | `delete_message` expunges |
| `billing` | `billing@grizzly-endeavors.com` | `billing@`, `admin@` | `delete_message` moves to `Deleted Items` (recoverable); use `move_message` to file handled mail |
| `support` | `support@goalaxi.com` | `support@goalaxi.com` | As `billing` |

The `claude` and `billing` passwords are the fields `claude_password` and `billing_password` on the 1Password item `platform-stalwart`; the `support` password is the `password` field on the item `goalaxi-support-mailbox`. `bin/grizzly-mail-mcp` holds the references.

A call naming a mailbox whose password was not loaded returns an error naming the missing 1Password field.

## Install

```
/plugin install grizzly-mail@grizzly-plugins
```

**Prerequisite:** the machine must hold the 1Password operator service-account token at `~/.config/op-tokens/operator` (override with `GRIZZLY_MAIL_OP_TOKEN_FILE`) and have the `op` CLI installed. The launcher reads `op://grizzly-platform/platform-stalwart/claude_password` (required), `.../billing_password` (optional), and `op://grizzly-platform/goalaxi-support-mailbox/password` (optional) once each per session. Without `claude_password` (or the token) the server refuses to start with a clear error; if either optional password is missing or unreadable, the launcher logs one line to stderr and starts without that mailbox. This plugin is only useful on Grizzly Endeavors machines.

## Tools

| Tool | What it does |
|---|---|
| `send_mail` | Send plain-text mail from the mailbox, as one of its addresses (`from_address`, default the primary; the domain is fixed for DMARC alignment), optionally with attachments; files a copy in `Sent Items` |
| `list_messages` | Compact newest-first listing of a folder (uid, flags, date, from, subject) |
| `read_message` | Headers + text body of one message by uid, truncated by default, with any attachments listed |
| `save_attachment` | Write one attachment to a path on disk and return where it landed |
| `delete_message` | Delete a message by uid — clean up test mail (in `billing`, moves to `Deleted Items` instead of expunging) |
| `move_message` | Move a message by uid between folders of one mailbox, creating the destination if absent — file handled mail |
| `list_folders` | List every folder in a mailbox |
| `wait_for_message` | Poll for a matching unseen message (junk folder included) — the receive half of a round-trip test |

Attachment contents are never inlined into tool output: `read_message` lists what a message carries, and `save_attachment` puts the bytes on disk to open with ordinary file tools. Bytes are written exactly as they arrived — archives stay packed, so unpack them yourself.

The bundled `grizzly-mail` skill carries the usage conventions: self-round-trip as the canonical check, cleanup discipline, the company mailbox as a record, and the stop-immediately rule on auth failures (repeated failed logins IP-ban the client on the server).

## How it works

`bin/grizzly-mail-mcp` (bash) fetches the mailbox passwords from 1Password once, then execs `server/grizzly_mail_mcp.py` — a single-file, stdlib-only Python server speaking newline-delimited JSON-RPC 2.0 over stdio. No SDK, no dependencies, no build step. Mail goes over implicit-TLS SMTP (465) and IMAPS (993) to the public `mail.grizzly-endeavors.com` host; connections are opened fresh per tool call.

The plugin's `bin/` directory lands on the Bash tool PATH like every plugin's; running `grizzly-mail-mcp` by hand just starts a JSON-RPC loop on stdin, which is also the smoke-test path:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | grizzly-mail-mcp
```

## Server-side account

The mailboxes are provisioned as IaC in the grizzly-platform repo (`ansible/playbooks/configure-stalwart.yml`); the operator runbook is `docs/runbooks/mail.md` there.
