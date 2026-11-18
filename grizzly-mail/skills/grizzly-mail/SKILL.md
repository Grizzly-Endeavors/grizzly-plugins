---
name: grizzly-mail
description: Conventions for the grizzly-mail MCP tools (send_mail, list_messages, read_message, save_attachment, delete_message, move_message, list_folders, wait_for_message) — the claude@grizzly-endeavors.com agent mailbox, the billing@/admin@ company mailbox and Goalaxi's support@goalaxi.com mailbox on the self-hosted Stalwart server. Use whenever sending or checking mail through those tools, reading, filing or answering company mail (bank, payment, government, vendor), triaging or answering Goalaxi support mail, pulling down an attachment, testing a mail flow end-to-end (invite emails, notifications, deliverability), or verifying that the platform's mail path works. Also covers what to do on an authentication failure.
---

# grizzly-mail: the agent, company and support mailboxes

The tools serve three mailboxes on the platform's Stalwart server, chosen with the optional `mailbox` argument on every tool (default `claude`):

- `claude` — `claude@grizzly-endeavors.com`, your own mailbox. It exists for testing and automation: proving mail flows work, receiving test messages from apps, checking deliverability. It is not a bulk sender and not a place to route anything important.
- `billing` — `billing@grizzly-endeavors.com`, which also receives `admin@grizzly-endeavors.com`. It is the company mailbox; see below. If a call reports the mailbox unavailable, tell Bear the 1Password field the error names and stop using that mailbox; restarting the server is the only way to load it.

- `support` — `support@goalaxi.com`, Goalaxi's support mailbox, where its legal pages send every rights request, opt-out, appeal and cancellation; see below. It can be unavailable in the same way as `billing`.

## The canonical end-to-end check

`send_mail` to `claude@grizzly-endeavors.com` (yourself), then `wait_for_message` on the subject. One round-trip proves SMTP submission, the SMTP2GO relay, own-MX inbound delivery, and IMAP all work. Delivery hairpins through the VPS and takes **~1–2 minutes** — that's normal, and `wait_for_message`'s default 120s timeout is sized for it. A timeout doesn't necessarily mean failure; one re-call to keep waiting is reasonable before investigating.

## Attachments

`read_message` lists a message's attachments after the body — index, filename, media type, size — and never inlines their contents. `save_attachment` takes that index plus a `dest` and writes the bytes to disk, returning the path to open with ordinary file tools.

Files are saved **exactly as they arrived**. A `.zip` or `.gz` stays packed, so run `unzip`/`gunzip` on the saved path yourself — a DMARC aggregate report, for instance, is zipped XML and takes a save then an unzip. `dest` can be a full file path or an existing directory to write into under the attachment's own name; an existing file is never clobbered unless you pass `overwrite`.

`send_mail` takes `attach` — a list of paths on this machine — capped at 20 MB total.

## Rules

- **Auth failure means STOP.** If any tool reports authentication failed, on any mailbox, do not call another mail tool and do not retry — tell Bear the 1Password field the error names may have drifted from Stalwart. Repeated failed logins IP-ban this machine's *public* IP on the server (the traffic hairpins via the VPS, so the LAN allowlist does not protect you), which takes down mail access for the whole household.
- **Clean up after yourself.** Test messages get `delete_message`d once the check is done — in the claude mailbox (`send_mail` also files a copy in `Sent Items`; delete that with `folder: "Sent Items"`), and (by asking Bear) anywhere you sent them.
- **Bear can read the claude mailbox.** Its Inbox and Sent Items are shared read-only into Bear's own webmail, so write mail as if a human will read it.
- **Don't spam real mailboxes.** One test message to `bearflinn@` when a human-visible check is genuinely needed; everything else round-trips through your own inbox.
- **`From:` must be one of the mailbox's own addresses** — `from_address` rejects anything else, and DMARC alignment is anchored on the domain.
- **Check the junk folder** when something seems undelivered — Stalwart's spam filter files some legit mail under `Junk Mail`. `wait_for_message` already looks there for you.

## The company mailbox (`billing`)

- Treat everything in it as the company's record: file handled mail with `move_message` into a folder named for its subject (e.g. `Bank`, `Taxes`, `Vendors`); `move_message` creates the folder when absent, and `list_folders` shows what exists.
- File handled mail with `move_message`. Use `delete_message` only for mail that is not a record (spam, phishing, duplicates); here it moves the message to `Deleted Items`, where it stays recoverable.
- Pass `mailbox: "billing"` on every call, including `wait_for_message`, `read_message` and `save_attachment`; without it the call goes to the claude mailbox.
- Treat mail you send from it as the company writing from a role address, not as you: sign as the company, make no personal commitments, and send only what the task asked for.
- Reply from the address the thread was sent to: read the message's `To`, and pass that address (`billing@` or `admin@`) as `from_address`.
- Don't use it for test round-trips; those stay in the claude mailbox.

## Goalaxi's support mailbox (`support`)

Pass `mailbox: "support"` on every call. It is a record like the company mailbox: file handled mail with `move_message`, and never use it for test round-trips.

- **Answer the simple mail yourself:** how something in the app works, where a setting is, how to cancel or export (both are in Settings), a sign-in link that didn't arrive, a bug report to acknowledge and file as an issue in the goalaxi repo. Write in Goalaxi's voice (the goalaxi repo's `brand/guidelines/voice.md`), and say only what the product and its published terms already say.
- **End every reply you write with the AI line,** on its own after the sign-off: "This reply was written by Goalaxi's AI support assistant. Reply and ask for a person, and one will answer."
- **Leave these for Bear, unanswered,** and tell him the same day with the sender's request in one line and the date it arrived: a privacy rights request (access, deletion, correction, opt-out, appeal), anything about a refund or a charge beyond pointing to Settings, a legal or press message, a complaint, anything from someone in distress, anyone who asks for a person, and anything you are unsure of. Rights requests run on legal clocks from the day they arrive (30 days for health data deletion, 45 for the others, two business days for a cancellation sent by email), so the arrival date matters.
- **Copy nothing a person wrote about their life out of the mailbox:** not into an issue, a commit, a wiki page or another tool. An issue filed from a support message describes the bug in your own words, with no name or address.

## When mail infrastructure itself misbehaves

The operator story (architecture, ingress path, ban recovery, restart procedure) lives in the grizzly-platform repo: `docs/runbooks/mail.md`. Provisioning more accounts is `docs/integration/mail.md`.
