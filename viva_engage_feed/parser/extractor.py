"""Record extractor for Viva Engage GraphQL feed edges.

Transforms raw GraphQL edge dicts into flat record dicts suitable for
rendering in the HTML report.
"""

from datetime import datetime, timezone
from typing import Optional

from .draft_js import draft_js_to_plaintext


def extract_record(edge: dict, sl_no: int) -> Optional[dict]:
    """Extract a flat record dict from a single GraphQL feed edge.

    The function tries to obtain the message body from (in order):

    1. ``edge["node"]["threadStarter"]["sharedMessage"]["body"]["serializedContentState"]``
    2. ``edge["node"]["threadStarter"]["languageSpecificContent"]["body"]["serializedContentState"]``

    Args:
        edge: A single edge dict from
            ``response["data"]["feedGroup"]["feed"]["threads"]["edges"]``.
        sl_no: Serial number to assign to this record.

    Returns:
        A dict with keys ``sl_no``, ``created_at``, ``message``,
        ``sender_name``, and ``sender_email``, or ``None`` if the required
        structure is absent.
    """
    try:
        thread_starter = edge["node"]["threadStarter"]

        # ── Created-at timestamp ───────────────────────────────────────────────
        raw_created_at: str = thread_starter["createdAt"]
        try:
            dt = datetime.fromisoformat(raw_created_at.replace("Z", "+00:00"))
            created_at = dt.strftime("%d-%b-%Y %H:%M UTC")
        except (ValueError, AttributeError):
            created_at = raw_created_at

        # ── Message body (prefer sharedMessage, fall back to languageSpecific) ─
        serialized: str = ""
        shared_message = thread_starter.get("sharedMessage")
        if shared_message:
            serialized = (
                shared_message.get("body", {}).get("serializedContentState", "")
            )

        if not serialized:
            lang_content = thread_starter.get("languageSpecificContent")
            if lang_content:
                serialized = (
                    lang_content.get("body", {}).get("serializedContentState", "")
                )

        message = draft_js_to_plaintext(serialized) if serialized else ""

        # ── Sender details ─────────────────────────────────────────────────────
        sender = thread_starter["sender"]
        sender_name: str = sender["displayName"]
        sender_email: str = sender["email"]

        return {
            "sl_no": sl_no,
            "created_at": created_at,
            "message": message,
            "sender_name": sender_name,
            "sender_email": sender_email,
        }
    except (KeyError, TypeError):
        return None
