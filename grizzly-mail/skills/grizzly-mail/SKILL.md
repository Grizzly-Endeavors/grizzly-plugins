---
name: grizzly-mail
description: Conventions for the grizzly-mail MCP tools (send_mail, list_messages, read_message, save_attachment, delete_message, wait_for_message) — the claude@grizzly-endeavors.com agent mailbox on the self-hosted Stalwart server. Use whenever sending or checking mail through those tools, reading or pulling down an attachment, testing a mail flow end-to-end (invite emails, notifications, deliverability), or verifying that the platform's mail path works. Also covers what to do on an authentication failure.
---

# grizzly-mail: the agent mailbox

You have your own mailbox: `claude@grizzly-endeavors.com` on the platform's Stalwart server. It exists for testing and automation — proving mail flows work, receiving test messages from apps, checking deliverability. It is not a bulk sender and not a place to route anything important.

## The canonical end-to-end check

`send_mail` to `claude@grizzly-endeavors.com` (yourself), then `wait_for_message` on the subject. One round-trip proves SMTP submission, the SMTP2GO relay, own-MX inbound delivery, and IMAP all work. Delivery hairpins through the VPS and takes **~1–2 minutes** — that's normal, and `wait_for_message`'s default 120s timeout is sized for it. A timeout doesn't necessarily mean failure; one re-call to keep waiting is reasonable before investigating.

## Attachments

`read_message` lists a message's attachments after the body — index, filename, media type, size — and never inlines their contents. `save_attachment` takes that index plus a `dest` and writes the bytes to disk, returning the path to open with ordinary file tools.

Files are saved **exactly as they arrived**. A `.zip` or `.gz` stays packed, so run `unzip`/`gunzip` on the saved path yourself — a DMARC aggregate report, for instance, is zipped XML and takes a save then an unzip. `dest` can be a full file path or an existing directory to write into under the attachment's own name; an existing file is never clobbered unless you pass `overwrite`.

`send_mail` takes `attach` — a list of paths on this machine — capped at 20 MB total.

## Rules

- **Auth failure means STOP.** If any tool reports authentication failed, do not call another mail tool and do not retry — tell Bear the 1Password `platform-stalwart/claude_password` may have drifted from Stalwart. Repeated failed logins IP-ban this machine's *public* IP on the server (the traffic hairpins via the VPS, so the LAN allowlist does not protect you), which takes down mail access for the whole household.
- **Clean up after yourself.** Test messages get `delete_message`d once the check is done — in this mailbox, and (by asking Bear) anywhere you sent them.
- **Don't spam real mailboxes.** One test message to `bearflinn@` when a human-visible check is genuinely needed; everything else round-trips through your own inbox.
- **`From:` is fixed** at `claude@grizzly-endeavors.com` by the server — DMARC alignment is anchored on the domain. Don't try to work around it.
- **Check the junk folder** when something seems undelivered — Stalwart's spam filter files some legit mail under `Junk Mail`. `wait_for_message` already looks there for you.

## When mail infrastructure itself misbehaves

The operator story (architecture, ingress path, ban recovery, restart procedure) lives in the grizzly-platform repo: `docs/runbooks/mail.md`. Provisioning more accounts is `docs/integration/mail.md`.
