"""Entry point for the Viva Engage Feed Extractor.

Fetches all group feed threads from the Microsoft Viva Engage GraphQL API,
converts each post to plain text, builds a styled HTML report table, and
saves it to disk.
"""

import sys

import config
from api.client import fetch_all_feed_pages
from parser.extractor import extract_record
from report.html_builder import build_html_table, save_html


def main() -> None:
    """Run the feed extraction and report generation pipeline."""
    if not config.BEARER_TOKEN:
        print(
            "Error: ENGAGE_BEARER_TOKEN is not set. "
            "Copy .env.example to .env and fill in your token.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not config.GROUP_ID:
        print(
            "Error: ENGAGE_GROUP_ID is not set. "
            "Copy .env.example to .env and fill in the group ID.",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── 1. Fetch all pages ─────────────────────────────────────────────────────
    pages = fetch_all_feed_pages(config.BEARER_TOKEN, config.GROUP_ID)
    total_pages = len(pages)

    # ── 2. Extract records ─────────────────────────────────────────────────────
    records = []
    sl_no = 1
    for page in pages:
        try:
            edges = page["data"]["feedGroup"]["feed"]["threads"]["edges"]
        except (KeyError, TypeError):
            continue
        for edge in edges:
            record = extract_record(edge, sl_no)
            if record is not None:
                records.append(record)
                sl_no += 1

    # ── 3. Build and save HTML report ──────────────────────────────────────────
    html = build_html_table(records)
    save_html(html, config.OUTPUT_FILE)

    # ── 4. Summary ────────────────────────────────────────────────────────────
    print(f"Total pages fetched  : {total_pages}")
    print(f"Total records extracted: {len(records)}")
    print(f"Output file          : {config.OUTPUT_FILE}")


if __name__ == "__main__":
    main()
