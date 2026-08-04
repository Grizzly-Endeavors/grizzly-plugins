#!/usr/bin/env python3
"""grizzly-mail MCP server: send/receive mail as the claude agent mailbox.

Stdlib-only. Speaks newline-delimited JSON-RPC 2.0 over stdio (initialize /
tools/list / tools/call / ping); stdout carries the protocol, stderr carries
diagnostics. Configuration and the mailbox password arrive via the process
environment, set by bin/grizzly-mail-mcp.

Connections are opened fresh per tool call (and per poll in wait_for_message)
and always closed: the server lives for a whole Claude session, and both
Stalwart and the fronting HAProxy drop idle sockets, so a persistent
connection would need stale-socket recovery in every tool for no real gain.

Auth discipline: exactly one login attempt per tool call, never a retry loop.
The desktop's traffic hairpins via the VPS, so Stalwart sees the home public
IP — outside the 10.0.0.0/8 ban allowlist — and repeated failed logins would
IP-ban the whole household's mail access.
"""

import email
import email.policy
import email.utils
import imaplib
import json
import mimetypes
import os
import pathlib
import re
import smtplib
import socket
import ssl
import sys
import time
import traceback
from email.message import EmailMessage
from html.parser import HTMLParser

HOST = os.environ["GRIZZLY_MAIL_HOST"]
USER = os.environ["GRIZZLY_MAIL_USER"]
PASSWORD = os.environ["GRIZZLY_MAIL_PASSWORD"]
SMTP_PORT = int(os.environ["GRIZZLY_MAIL_SMTP_PORT"])
IMAP_PORT = int(os.environ["GRIZZLY_MAIL_IMAP_PORT"])
DOMAIN = USER.rsplit("@", 1)[1]

SERVER_INFO = {"name": "grizzly-mail", "version": "0.2.0"}
FALLBACK_PROTOCOL = "2024-11-05"
JUNK_FOLDER = "Junk Mail"

# Outbound attachments are capped well under the relay's own ceiling so an
# oversized send fails here, instantly and legibly, instead of after a slow
# upload ending in an SMTP rejection.
MAX_ATTACH_BYTES = 20 * 1024 * 1024

# Media types for the compressions mimetypes reports as an encoding. For a
# name like report.xml.gz it returns the *inner* type (application/xml) plus
# "gzip", but the attached bytes are the container — labelling them by the
# inner type would tell the recipient to parse gzip as XML.
DEFAULT_TYPE = "application/octet-stream"
ENCODING_TYPES = {
    "gzip": "application/gzip",
    "bzip2": "application/x-bzip2",
    "xz": "application/x-xz",
    "compress": "application/x-compress",
    "br": "application/x-brotli",
}

AUTH_ERROR = (
    f"authentication failed for {USER} — the password in 1Password "
    "(platform-stalwart/claude_password) may not match Stalwart, or the "
    "account isn't provisioned. STOP: do not retry — repeated failures will "
    "IP-ban this machine's public IP on the mail server (recovery is a "
    "port-forward + delete BlockedIp, see grizzly-platform "
    "docs/runbooks/mail.md). Fix the credential, then restart the MCP server."
)
NETWORK_ERROR = (
    f"cannot reach {HOST} — network or VPS-ingress issue (this can be "
    "transient; a single re-call is safe). See grizzly-platform "
    "docs/runbooks/mail.md for the mail path."
)
RESET_ERROR = (
    "connection reset right after connect — if GRIZZLY_MAIL_HOST was "
    "overridden to an internal address, use the public host: the internal "
    "listeners expect a PROXY-protocol header and reset direct connections."
)


# ---------------------------------------------------------------------------
# mail helpers

def imap_connect():
    """Fresh authenticated IMAP connection. One login attempt, no retries."""
    conn = imaplib.IMAP4_SSL(HOST, IMAP_PORT, timeout=30)
    try:
        conn.login(USER, PASSWORD)
    except imaplib.IMAP4.error:
        try:
            conn.logout()
        except Exception:
            pass
        raise
    return conn


def imap_close(conn):
    try:
        conn.logout()
    except Exception:
        pass


def select_folder(conn, folder, readonly):
    typ, data = conn.select(f'"{folder}"', readonly=readonly)
    if typ != "OK":
        detail = (data[0] or b"").decode(errors="replace")
        raise ToolError(
            f"cannot open folder {folder!r} ({detail}) — folder names are "
            "case-sensitive and may contain spaces (e.g. \"Junk Mail\", "
            "\"Sent Items\")."
        )


class ToolError(Exception):
    """A tool failure with a message already fit for the caller."""


def parse_fetch_headers(data):
    """Yield (uid, flags, message) from a UID FETCH response with headers."""
    for item in data:
        if not isinstance(item, tuple) or len(item) < 2:
            continue
        meta = item[0].decode(errors="replace")
        uid_m = re.search(r"UID (\d+)", meta)
        if not uid_m:
            continue
        flags_m = re.search(r"FLAGS \(([^)]*)\)", meta)
        msg = email.message_from_bytes(item[1], policy=email.policy.default)
        yield uid_m.group(1), (flags_m.group(1) if flags_m else ""), msg


def summary_line(uid, flags, msg, folder):
    unseen = "" if "\\Seen" in flags else " [unseen]"
    date = msg.get("Date", "")
    try:
        date = email.utils.parsedate_to_datetime(date).strftime("%Y-%m-%d %H:%M")
    except Exception:
        pass
    sender = str(msg.get("From", "?"))
    subject = str(msg.get("Subject", "(no subject)"))
    where = "" if folder == "INBOX" else f" (in {folder})"
    return f"uid={uid}{unseen} {date} {sender} | {subject}{where}"


def fetch_summaries(conn, folder, unseen_only, limit):
    """Newest-first summary lines for a folder. Connection must be logged in."""
    select_folder(conn, folder, readonly=True)
    typ, data = conn.uid("search", None, "UNSEEN" if unseen_only else "ALL")
    uids = data[0].split() if typ == "OK" and data[0] else []
    total = len(uids)
    wanted = [u.decode() for u in uids[-limit:]][::-1]
    lines = []
    if wanted:
        typ, data = conn.uid(
            "fetch", ",".join(wanted),
            "(FLAGS BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])",
        )
        by_uid = {uid: (flags, msg)
                  for uid, flags, msg in parse_fetch_headers(data)}
        lines = [summary_line(u, *by_uid[u], folder)
                 for u in wanted if u in by_uid]
    return lines, total


class TextExtractor(HTMLParser):
    """Minimal HTML→text: body text with tags dropped, scripts/styles skipped."""

    SKIP = {"script", "style", "head"}

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if not self.skip_depth and data.strip():
            self.parts.append(data.strip())

    def text(self):
        return "\n".join(self.parts)


def message_body_text(msg):
    body = msg.get_body(preferencelist=("plain", "html"))
    if body is None:
        return "(no text or html body part)"
    content = body.get_content()
    if body.get_content_type() == "text/html":
        extractor = TextExtractor()
        extractor.feed(content)
        content = extractor.text() or "(html body with no extractable text)"
    return content


def fetch_raw_message(conn, uid, folder, readonly=True):
    """Raw bytes of one message by uid. Connection must be logged in."""
    select_folder(conn, folder, readonly=readonly)
    typ, data = conn.uid("fetch", uid, "(BODY.PEEK[])")
    raw = next((item[1] for item in data
                if isinstance(item, tuple) and len(item) > 1), None)
    if typ != "OK" or raw is None:
        raise ToolError(
            f"uid {uid} not found in {folder} (already deleted or wrong "
            "folder — list_messages to check)."
        )
    return raw


# ---------------------------------------------------------------------------
# attachments

def attachment_parts(msg):
    """Attachment parts in the order save_attachment's 1-based index uses.

    A single-part message that is not text carries its payload directly
    rather than in a sub-part, and iter_attachments would yield nothing for
    it — so it counts as the message's one attachment.
    """
    if not msg.is_multipart():
        return [] if msg.get_content_maintype() == "text" else [msg]
    return list(msg.iter_attachments())


def human_size(count):
    size = float(count)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024


def attachment_manifest(parts, uid):
    """Listing of a message's attachments, empty when it has none."""
    if not parts:
        return ""
    lines = [f"attachments ({len(parts)}):"]
    for index, part in enumerate(parts, 1):
        payload = part.get_payload(decode=True) or b""
        lines.append(
            f"  [{index}] {part.get_filename() or '(no filename)'}  "
            f"{part.get_content_type()}  {human_size(len(payload))}  "
            f"({part.get_content_disposition() or 'unspecified'})"
        )
    lines.append(
        f"save_attachment with uid={uid} and an index writes one to a path "
        "you choose. Bytes are written exactly as they arrived, so unpack "
        "archives (unzip, gunzip) yourself afterwards."
    )
    return "\n".join(lines)


def safe_attachment_name(part, index):
    """A filesystem-safe basename for an attachment.

    The filename in a message is chosen by whoever sent it, so it is never
    treated as a path: only the basename survives, and anything left that
    would still escape or resolve oddly falls back to a generated name.
    """
    raw = (part.get_filename() or "").replace("\\", "/").replace("\x00", "")
    name = os.path.basename(raw).strip()
    if not name or name in (".", ".."):
        suffix = mimetypes.guess_extension(part.get_content_type()) or ".bin"
        name = f"attachment-{index}{suffix}"
    return name


def resolve_dest(dest, filename):
    """Absolute path to write to, given a caller's dest and the safe name.

    A dest naming a directory (or ending in a separator) takes the
    attachment's own name; anything else is used verbatim as the file path.
    """
    path = pathlib.Path(dest).expanduser()
    if dest.endswith(("/", os.sep)) or path.is_dir():
        path = path / filename
    if not path.parent.is_dir():
        raise ToolError(
            f"no directory {path.parent} to write into — create it first, or "
            "pass a dest inside a directory that already exists."
        )
    return path


# ---------------------------------------------------------------------------
# tools

def tool_send_mail(args):
    to = args["to"]
    msg = EmailMessage()
    msg["From"] = USER  # fixed sender: DMARC alignment is anchored on DOMAIN
    msg["To"] = to
    msg["Subject"] = args["subject"]
    msg["Message-ID"] = email.utils.make_msgid(domain=DOMAIN)
    msg["Date"] = email.utils.formatdate(localtime=True)
    if args.get("cc"):
        msg["Cc"] = args["cc"]
    if args.get("reply_to"):
        msg["Reply-To"] = args["reply_to"]
    msg.set_content(args["body"])
    attached = attach_files(msg, args.get("attach") or [])
    with smtplib.SMTP_SSL(HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.login(USER, PASSWORD)
        smtp.send_message(msg)
    note = f" with {len(attached)} attachment(s): {', '.join(attached)}" \
        if attached else ""
    return f"sent {msg['Message-ID']} to {to}{note}"


def attach_files(msg, paths):
    """Attach each path to msg, returning the filenames used."""
    names = []
    total = 0
    for given in paths:
        path = pathlib.Path(given).expanduser()
        if not path.is_file():
            raise ToolError(
                f"cannot attach {given} — it is not a readable file (check "
                "the path; it must already exist on this machine)."
            )
        data = path.read_bytes()
        total += len(data)
        if total > MAX_ATTACH_BYTES:
            raise ToolError(
                f"attachments exceed {human_size(MAX_ATTACH_BYTES)} in total "
                f"at {path.name} — nothing was sent. Send fewer or smaller "
                "files; the relay rejects oversized messages."
            )
        ctype, encoding = mimetypes.guess_type(path.name)
        if encoding:
            ctype = ENCODING_TYPES.get(encoding, DEFAULT_TYPE)
        maintype, _, subtype = (ctype or DEFAULT_TYPE).partition("/")
        msg.add_attachment(data, maintype=maintype, subtype=subtype,
                           filename=path.name)
        names.append(path.name)
    return names


def tool_list_messages(args):
    folder = args.get("folder", "INBOX")
    limit = min(int(args.get("limit", 10)), 50)
    unseen_only = bool(args.get("unseen_only", False))
    conn = imap_connect()
    try:
        lines, total = fetch_summaries(conn, folder, unseen_only, limit)
    finally:
        imap_close(conn)
    which = "unseen" if unseen_only else "message(s)"
    if not lines:
        return f"no {which} in {folder}"
    return "\n".join(lines + [f"{len(lines)} of {total} {which} in {folder}"])


def tool_read_message(args):
    uid = str(args["uid"])
    folder = args.get("folder", "INBOX")
    max_bytes = int(args.get("max_bytes", 4096))
    mark_seen = bool(args.get("mark_seen", True))
    conn = imap_connect()
    try:
        raw = fetch_raw_message(conn, uid, folder, readonly=not mark_seen)
        if mark_seen:
            conn.uid("store", uid, "+FLAGS", r"(\Seen)")
    finally:
        imap_close(conn)
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    headers = "\n".join(
        f"{name}: {msg[name]}" for name in
        ("From", "To", "Cc", "Subject", "Date", "Message-ID") if msg[name]
    )
    body = message_body_text(msg)
    encoded = body.encode()
    if len(encoded) > max_bytes:
        body = encoded[:max_bytes].decode(errors="ignore") + (
            f"\n[truncated — {max_bytes} of {len(encoded)} bytes; "
            f"re-call with max_bytes={len(encoded)}]"
        )
    # The manifest follows the truncated body rather than sharing its budget:
    # a long message must not be able to hide that it carried attachments.
    manifest = attachment_manifest(attachment_parts(msg), uid)
    return f"{headers}\n\n{body}" + (f"\n\n{manifest}" if manifest else "")


def tool_save_attachment(args):
    uid = str(args["uid"])
    folder = args.get("folder", "INBOX")
    index = int(args["index"])
    dest = args["dest"]
    overwrite = bool(args.get("overwrite", False))
    conn = imap_connect()
    try:
        raw = fetch_raw_message(conn, uid, folder, readonly=True)
    finally:
        imap_close(conn)
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    parts = attachment_parts(msg)
    if not parts:
        raise ToolError(f"uid {uid} in {folder} has no attachments.")
    if not 1 <= index <= len(parts):
        raise ToolError(
            f"no attachment [{index}] on uid {uid} — it has {len(parts)}, "
            f"indexed 1-{len(parts)} (read_message lists them)."
        )
    part = parts[index - 1]
    payload = part.get_payload(decode=True)
    if payload is None:
        raise ToolError(
            f"attachment [{index}] on uid {uid} has no decodable content "
            f"(content-type {part.get_content_type()})."
        )
    path = resolve_dest(dest, safe_attachment_name(part, index))
    if path.exists() and not overwrite:
        raise ToolError(
            f"{path} already exists and was left untouched — pass "
            "overwrite=true to replace it, or choose another dest."
        )
    path.write_bytes(payload)
    return (
        f"saved attachment [{index}] of uid={uid} to {path} "
        f"({human_size(len(payload))}, {part.get_content_type()}) — written "
        "as-is, so unpack it yourself if it is an archive"
    )


def tool_delete_message(args):
    uid = str(args["uid"])
    folder = args.get("folder", "INBOX")
    conn = imap_connect()
    try:
        select_folder(conn, folder, readonly=False)
        typ, data = conn.uid("search", None, f"UID {uid}")
        if typ != "OK" or not data[0]:
            raise ToolError(
                f"uid {uid} not found in {folder} (already deleted or wrong "
                "folder — list_messages to check)."
            )
        conn.uid("store", uid, "+FLAGS", r"(\Deleted)")
        conn.expunge()
    finally:
        imap_close(conn)
    return f"deleted uid={uid} from {folder}"


def tool_wait_for_message(args):
    subject_contains = args.get("subject_contains", "")
    from_contains = args.get("from_contains", "")
    if not subject_contains and not from_contains:
        raise ToolError(
            "give at least one of subject_contains / from_contains."
        )
    folder = args.get("folder", "INBOX")
    timeout_s = min(int(args.get("timeout_seconds", 120)), 300)
    poll = max(int(args.get("poll_interval", 10)), 2)
    folders = [folder] + ([JUNK_FOLDER] if folder != JUNK_FOLDER else [])

    def match(flags, msg):
        subject = str(msg.get("Subject", "")).lower()
        sender = str(msg.get("From", "")).lower()
        return ((not subject_contains or subject_contains.lower() in subject)
                and (not from_contains or from_contains.lower() in sender))

    deadline = time.monotonic() + timeout_s
    while True:
        conn = imap_connect()
        try:
            for fld in folders:
                select_folder(conn, fld, readonly=True)
                typ, data = conn.uid("search", None, "UNSEEN")
                uids = data[0].split() if typ == "OK" and data[0] else []
                if not uids:
                    continue
                typ, data = conn.uid(
                    "fetch", b",".join(uids).decode(),
                    "(FLAGS BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])",
                )
                for uid, flags, msg in parse_fetch_headers(data):
                    if match(flags, msg):
                        note = ("" if fld == folder else
                                "\n(note: landed in the junk folder — the "
                                "spam filter files some legit mail there)")
                        return summary_line(uid, flags, msg, fld) + note
        finally:
            imap_close(conn)
        if time.monotonic() >= deadline:
            raise ToolError(
                f"no unseen message matching "
                f"subject~{subject_contains!r} from~{from_contains!r} in "
                f"{' / '.join(folders)} after {timeout_s}s — the send may "
                "have failed, or delivery is slow (self-hairpin round-trips "
                "run ~1–2 min; re-call to keep waiting)."
            )
        time.sleep(min(poll, max(deadline - time.monotonic(), 0.1)))


TOOLS = [
    {
        "name": "send_mail",
        "description": (
            f"Send a plain-text email as {USER}. The From address is fixed "
            "(DMARC alignment). Returns the Message-ID. Delivery to any "
            "mailbox on the platform (including this one) takes ~1-2 minutes "
            "— pair with wait_for_message for a round-trip check."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient address"},
                "subject": {"type": "string"},
                "body": {"type": "string", "description": "Plain-text body"},
                "cc": {"type": "string", "description": "Optional Cc address"},
                "reply_to": {"type": "string",
                             "description": "Optional Reply-To address"},
                "attach": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Optional paths to files on this machine to attach. "
                        "Total size is capped at "
                        f"{human_size(MAX_ATTACH_BYTES)}."
                    ),
                },
            },
            "required": ["to", "subject", "body"],
        },
    },
    {
        "name": "list_messages",
        "description": (
            "List messages in a mailbox folder, newest first, one compact "
            "line each (uid, flags, date, from, subject). Folders: INBOX, "
            "\"Junk Mail\", \"Sent Items\", Drafts, \"Deleted Items\"."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "folder": {"type": "string", "default": "INBOX"},
                "limit": {"type": "integer", "default": 10, "maximum": 50},
                "unseen_only": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "read_message",
        "description": (
            "Read one message by uid: headers plus the text body (html is "
            "stripped to text). Output is truncated at max_bytes; the "
            "truncation note says how to fetch the rest. Any attachments are "
            "listed after the body with the index save_attachment takes — "
            "their contents are never inlined."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "folder": {"type": "string", "default": "INBOX"},
                "max_bytes": {"type": "integer", "default": 4096},
                "mark_seen": {"type": "boolean", "default": True},
            },
            "required": ["uid"],
        },
    },
    {
        "name": "save_attachment",
        "description": (
            "Write one attachment to a path on this machine and return where "
            "it landed, so it can be opened with ordinary file tools. Get the "
            "index from read_message. Bytes are saved exactly as they "
            "arrived — archives (.zip, .gz) are not unpacked, so run unzip or "
            "gunzip on the saved file yourself."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "index": {
                    "type": "integer",
                    "description": "1-based index from read_message's listing",
                },
                "dest": {
                    "type": "string",
                    "description": (
                        "Where to write it: a full file path, or an existing "
                        "directory to write into under the attachment's own "
                        "name"
                    ),
                },
                "folder": {"type": "string", "default": "INBOX"},
                "overwrite": {
                    "type": "boolean",
                    "default": False,
                    "description": "Replace dest if a file is already there",
                },
            },
            "required": ["uid", "index", "dest"],
        },
    },
    {
        "name": "delete_message",
        "description": "Delete one message by uid (flag + expunge). "
                       "Clean up test mail when done with it.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "folder": {"type": "string", "default": "INBOX"},
            },
            "required": ["uid"],
        },
    },
    {
        "name": "wait_for_message",
        "description": (
            "Poll for an unseen message matching subject and/or sender "
            "substrings (case-insensitive); the junk folder is checked too. "
            "Returns the match's summary line (with uid) or errors on "
            "timeout. This is the round-trip half of send_mail."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject_contains": {"type": "string"},
                "from_contains": {"type": "string"},
                "folder": {"type": "string", "default": "INBOX"},
                "timeout_seconds": {"type": "integer", "default": 120,
                                    "maximum": 300},
                "poll_interval": {"type": "integer", "default": 10},
            },
        },
    },
]

TOOL_HANDLERS = {
    "send_mail": tool_send_mail,
    "list_messages": tool_list_messages,
    "read_message": tool_read_message,
    "save_attachment": tool_save_attachment,
    "delete_message": tool_delete_message,
    "wait_for_message": tool_wait_for_message,
}


def error_text(exc):
    """Map an exception to actionable caller-facing text."""
    if isinstance(exc, ToolError):
        return str(exc)
    if isinstance(exc, smtplib.SMTPAuthenticationError):
        return AUTH_ERROR
    if isinstance(exc, imaplib.IMAP4.error):
        text = str(exc)
        if re.search(r"auth|login|credential", text, re.IGNORECASE):
            return AUTH_ERROR
        return f"IMAP error: {text}"
    if isinstance(exc, ConnectionResetError):
        return RESET_ERROR
    if isinstance(exc, (socket.timeout, TimeoutError, ConnectionRefusedError,
                        socket.gaierror, ssl.SSLError, OSError)):
        return f"{NETWORK_ERROR} ({type(exc).__name__}: {exc})"
    return f"{type(exc).__name__}: {exc}"


# ---------------------------------------------------------------------------
# JSON-RPC plumbing

def handle(method, params):
    if method == "initialize":
        return {
            "protocolVersion": params.get("protocolVersion",
                                          FALLBACK_PROTOCOL),
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        }
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        name = params.get("name", "")
        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            raise ToolError(f"unknown tool {name!r}")
        try:
            text = handler(params.get("arguments") or {})
            is_error = False
        except Exception as exc:  # every failure becomes visible tool output
            traceback.print_exc(file=sys.stderr)
            text = error_text(exc)
            is_error = True
        return {"content": [{"type": "text", "text": text}],
                "isError": is_error}
    if method == "ping":
        return {}
    return None  # unknown method sentinel


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as exc:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {
                "code": -32700, "message": f"parse error: {exc}"}}),
                flush=True)
            continue
        req_id = req.get("id")
        method = req.get("method", "")
        result = handle(method, req.get("params") or {})
        if req_id is None:
            continue  # notification — never respond
        if result is None:
            response = {"jsonrpc": "2.0", "id": req_id, "error": {
                "code": -32601, "message": f"method not found: {method}"}}
        else:
            response = {"jsonrpc": "2.0", "id": req_id, "result": result}
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
