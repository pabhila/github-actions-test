"""Draft.js serialized content state parser.

Converts Draft.js ``serializedContentState`` JSON strings into plain text.
"""

import json


def draft_js_to_plaintext(serialized_content_state: str) -> str:
    """Convert a Draft.js serialized content state JSON string to plain text.

    Block type mapping:

    * ``unordered-list-item`` → prefixed with ``• ``
    * ``ordered-list-item``   → prefixed with ``- ``
    * All other types         → raw text, no prefix

    Lines are joined with ``\\n``.  Returns an empty string on any parse error.

    Args:
        serialized_content_state: JSON string as stored in the
            ``body.serializedContentState`` field of a Viva Engage message.

    Returns:
        Plain-text representation of the content, or ``""`` on error.
    """
    try:
        content = json.loads(serialized_content_state)
        blocks = content.get("blocks", [])
        lines = []
        for block in blocks:
            text = block.get("text", "")
            block_type = block.get("type", "")
            if block_type == "unordered-list-item":
                lines.append(f"• {text}")
            elif block_type == "ordered-list-item":
                lines.append(f"- {text}")
            else:
                lines.append(text)
        return "\n".join(lines)
    except Exception:  # noqa: BLE001
        return ""
