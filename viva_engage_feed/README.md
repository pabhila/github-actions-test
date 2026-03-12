# Viva Engage Feed Extractor

A Python tool that fetches posts from the **Microsoft Viva Engage (Yammer)
GraphQL API**, parses the Draft.js `serializedContentState` message bodies
into plain text, and generates a styled HTML report table.

---

## Project Structure

```
viva_engage_feed/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── api/
│   ├── __init__.py
│   └── client.py
├── parser/
│   ├── __init__.py
│   ├── draft_js.py
│   └── extractor.py
├── report/
│   ├── __init__.py
│   └── html_builder.py
└── main.py
```

---

## Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repo-url>
   cd viva_engage_feed
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your Bearer token and group ID:
   ```
   ENGAGE_BEARER_TOKEN=<your_bearer_token>
   ENGAGE_GROUP_ID=<base64_encoded_group_id>
   OUTPUT_FILE=feed_report.html
   ```

---

## How to Run

```bash
python main.py
```

The script will:

1. Load configuration from `.env`.
2. Fetch all pages of group feed threads from the Viva Engage GraphQL API.
3. Parse each message body from Draft.js JSON to plain text.
4. Build a styled HTML table of all posts.
5. Save the report and print a summary to the console.

---

## Output

An HTML file (default: `feed_report.html`) is created in the working
directory.  It contains a responsive table with the following columns:

| Column | Description |
|--------|-------------|
| SL No | Serial number |
| Created | Post timestamp (UTC) |
| Message | Plain-text post body |
| Sender Name | Display name of the author |
| Sender Email | Clickable `mailto:` link |

---

## Refreshing the Bearer Token

The Bearer token is a short-lived JWT that typically expires within an hour.

To obtain a fresh token:

1. Open [https://engage.cloud.microsoft](https://engage.cloud.microsoft) in
   your browser.
2. Open **DevTools** (F12) → **Network** tab.
3. Navigate to the target group feed.
4. Find a request to `graphql?operationName=FeedGroupNestedClients`.
5. Copy the value of the `authorization` header (omit the leading `Bearer `
   prefix).
6. Paste it into the `ENGAGE_BEARER_TOKEN` variable in your `.env` file.

---

## Security

> ⚠️ **Never commit `.env` to version control.**
>
> Your `.env` file contains a live credential. It is listed in `.gitignore`
> to prevent accidental commits. Rotate the token if it has been exposed.
