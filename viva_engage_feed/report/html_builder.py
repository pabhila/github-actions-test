"""HTML report builder for the Viva Engage Feed Extractor.

Generates a styled HTML table from a list of extracted feed records and
writes it to disk.
"""


def escape_html(text: str) -> str:
    """Escape special HTML characters in *text*.

    Replaces ``&``, ``<``, ``>``, and ``"`` with their HTML entity equivalents.

    Args:
        text: Raw string that may contain HTML-special characters.

    Returns:
        Escaped string safe to embed in HTML content or attribute values.
    """
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def plaintext_to_html_lines(text: str) -> str:
    """Convert newline-separated plain text to HTML-escaped, ``<br>``-joined lines.

    Args:
        text: Plain text with ``\\n`` line separators.

    Returns:
        HTML string where each line is escaped and lines are joined with
        ``<br>``.
    """
    lines = text.split("\n")
    return "<br>".join(escape_html(line) for line in lines)


def build_html_table(records: list) -> str:
    """Build a complete, styled HTML page containing a feed records table.

    The page includes:

    * A ``<table>`` with columns **SL No**, **Created**, **Message**,
      **Sender Name**, and **Sender Email**.
    * A blue header row (``#0078d4``, white text).
    * Alternating row background colour (``#f3f9ff``).
    * Row hover highlight (``#e5f1fb``).
    * Sender email rendered as a ``mailto:`` hyperlink.
    * Responsive column widths via ``<colgroup>``.

    Args:
        records: List of record dicts produced by
            :func:`parser.extractor.extract_record`.

    Returns:
        A complete ``<!DOCTYPE html>`` document as a string, or
        ``"<p>No records found.</p>"`` when *records* is empty.
    """
    if not records:
        return "<p>No records found.</p>"

    rows_html = []
    for idx, rec in enumerate(records):
        row_style = ' style="background-color:#f3f9ff;"' if idx % 2 == 1 else ""
        email = escape_html(rec.get("sender_email", ""))
        rows_html.append(
            f'  <tr{row_style}>\n'
            f'    <td>{rec.get("sl_no", "")}</td>\n'
            f'    <td>{escape_html(rec.get("created_at", ""))}</td>\n'
            f'    <td>{plaintext_to_html_lines(rec.get("message", ""))}</td>\n'
            f'    <td>{escape_html(rec.get("sender_name", ""))}</td>\n'
            f'    <td><a href="mailto:{email}">{email}</a></td>\n'
            f'  </tr>'
        )

    rows = "\n".join(rows_html)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Viva Engage Feed Report</title>
  <style>
    body {{
      font-family: Segoe UI, Arial, sans-serif;
      margin: 24px;
      color: #333;
    }}
    h1 {{
      color: #0078d4;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th {{
      background-color: #0078d4;
      color: #fff;
      padding: 10px 12px;
      text-align: left;
    }}
    td {{
      padding: 8px 12px;
      border-bottom: 1px solid #dde3e8;
      vertical-align: top;
    }}
    tr:hover td {{
      background-color: #e5f1fb;
    }}
    a {{
      color: #0078d4;
    }}
  </style>
</head>
<body>
  <h1>Viva Engage Feed Report</h1>
  <table>
    <colgroup>
      <col style="width:4%">
      <col style="width:12%">
      <col style="width:54%">
      <col style="width:15%">
      <col style="width:15%">
    </colgroup>
    <thead>
      <tr>
        <th>SL No</th>
        <th>Created</th>
        <th>Message</th>
        <th>Sender Name</th>
        <th>Sender Email</th>
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>"""


def save_html(html: str, filepath: str) -> None:
    """Write *html* to *filepath* and print a confirmation message.

    Args:
        html: HTML string to write.
        filepath: Destination file path (relative or absolute).
    """
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Report saved to: {filepath}")
