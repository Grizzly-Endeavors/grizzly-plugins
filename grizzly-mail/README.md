# grizzly-mail

An MCP server giving Claude Code its own mailbox: `claude@grizzly-endeavors.com` on the self-hosted Stalwart mail server. Built for end-to-end mail testing — prove a mail flow works by actually sending and receiving.

## Install

```
/plugin install grizzly-mail@grizzly-plugins
```

**Prerequisite:** the machine must hold the 1Password operator service-account token at `~/.config/op-tokens/operator` (override with `GRIZZLY_MAIL_OP_TOKEN_FILE`) and have the `op` CLI installed. The launcher reads the mailbox password from `op://grizzly-platform/platform-stalwart/claude_password` once per session; without the token the server refuses to start with a clear error. This plugin is only useful on Grizzly Endeavors machines.

## Tools

| Tool | What it does |
|---|---|
| `send_mail` | Send plain-text mail as `claude@grizzly-endeavors.com` (From is fixed for DMARC alignment) |
| `list_messages` | Compact newest-first listing of a folder (uid, flags, date, from, subject) |
| `read_message` | Headers + text body of one message by uid, truncated by default |
| `delete_message` | Delete a message by uid — clean up test mail |
| `wait_for_message` | Poll for a matching unseen message (junk folder included) — the receive half of a round-trip test |

The bundled `grizzly-mail` skill carries the usage conventions: self-round-trip as the canonical check, cleanup discipline, and the stop-immediately rule on auth failures (repeated failed logins IP-ban the client on the server).

## How it works

`bin/grizzly-mail-mcp` (bash) fetches the mailbox password from 1Password once, then execs `server/grizzly_mail_mcp.py` — a single-file, stdlib-only Python server speaking newline-delimited JSON-RPC 2.0 over stdio. No SDK, no dependencies, no build step. Mail goes over implicit-TLS SMTP (465) and IMAPS (993) to the public `mail.grizzly-endeavors.com` host; connections are opened fresh per tool call.

The plugin's `bin/` directory lands on the Bash tool PATH like every plugin's; running `grizzly-mail-mcp` by hand just starts a JSON-RPC loop on stdin, which is also the smoke-test path:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | grizzly-mail-mcp
```

## Server-side account

The mailbox is provisioned as IaC in the grizzly-platform repo (`ansible/playbooks/configure-stalwart.yml`); the operator runbook is `docs/runbooks/mail.md` there.
