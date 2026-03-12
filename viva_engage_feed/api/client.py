"""HTTP client for the Microsoft Viva Engage (Yammer) GraphQL API.

Provides functions to fetch group feed threads using the
FeedGroupNestedClients persisted query.
"""

import json
import uuid
from typing import Optional

import requests

# Persisted query SHA-256 hash
_PERSISTED_QUERY_HASH = (
    "1253c0bcf0be35364c89e86ae33e7723b61fdaa67d53102e766c5d4ef337197b"
)

_YAMMER_TREATMENTS = [
    {"project": "ClientForward", "key": "MultiTenantOrganization", "value": "true"},
    {"project": "ClientForward", "key": "CopilotAdoptionCommunityAdminFRE", "value": "true"},
    {"project": "ClientForward", "key": "GuidedAdminNotificationsLandingPage", "value": "true"},
    {"project": "ClientForward", "key": "InformationBarriersPhase0", "value": "true"},
    {"project": "ClientForward", "key": "LoadThreadDataWhileRouting", "value": "control"},
    {"project": "ClientForward", "key": "ModerationAgentBlockPost", "value": "true"},
    {"project": "ClientForward", "key": "StorylineEmptyFeedTeamsExperience", "value": "enabled"},
    {"project": "ClientForward", "key": "SuggestedContentGuidedAdminExperience", "value": "true"},
    {"project": "CrossPlatform", "key": "HideUserGlobalToggle", "value": "true"},
]

_API_URL = (
    "https://engage.cloud.microsoft/graphql?operationName=FeedGroupNestedClients"
)


def fetch_feed_group_nested_clients(
    bearer_token: str,
    group_id: str,
    older_than: Optional[str] = None,
    thread_count: int = 4,
    reply_count: int = 2,
    sort_replies_by: str = "UPVOTE_RANK_THEN_CREATED_AT",
    sort_threads_by: str = "CREATED_AT",
    group_feed_type: str = "ALL",
    content_target_language: str = "en-us",
    request_id: Optional[str] = None,
) -> dict:
    """Fetch a single page of group feed threads from the Viva Engage GraphQL API.

    Args:
        bearer_token: OAuth2 Bearer token (without the ``Bearer `` prefix).
        group_id: Base64-encoded group ID.
        older_than: Pagination cursor from a previous response.  Pass ``None``
            to fetch the first page.
        thread_count: Number of threads to return per page (default 4).
        reply_count: Number of replies per thread (default 2).
        sort_replies_by: Reply sort order (default
            ``"UPVOTE_RANK_THEN_CREATED_AT"``).
        sort_threads_by: Thread sort order (default ``"CREATED_AT"``).
        group_feed_type: Feed type filter, e.g. ``"ALL"`` (default).
        content_target_language: BCP-47 language tag for translated content
            (default ``"en-us"``).
        request_id: Optional tracing UUID; auto-generated when omitted.

    Returns:
        Parsed JSON response as a Python :class:`dict`.

    Raises:
        requests.HTTPError: On non-2xx HTTP responses.
        ValueError: If the response body is not valid JSON.
    """
    variables: dict = {
        "threadCount": thread_count,
        "replyCount": reply_count,
        "sortRepliesBy": sort_replies_by,
        "sortThreadsBy": sort_threads_by,
        "requestContentInTargetLanguage": True,
        "contentTargetLanguage": content_target_language,
        "groupId": group_id,
        "groupFeedType": group_feed_type,
        "includeSenderBadges": True,
        "includeHiddenForNetworkInDiscovery": True,
        "includeViewerHasBookmarked": True,
        "includeOriginNetworkBadge": True,
        "includeUserHideFields": True,
        "includeGroupFeedLastVisitedAt": False,
        "includeGroupFeedLastVisitedIds": False,
        "includeVerifiedReply": True,
        "includeMessageContentSourceFile": True,
    }

    if older_than:
        variables["olderThan"] = older_than

    payload = {
        "operationName": "FeedGroupNestedClients",
        "variables": variables,
        "extensions": {
            "yammerTreatments": {
                "version": "1",
                "treatments": _YAMMER_TREATMENTS,
            },
            "persistedQuery": {
                "version": 1,
                "sha256Hash": _PERSISTED_QUERY_HASH,
            },
        },
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.5",
        "authorization": f"Bearer {bearer_token}",
        "content-type": "application/json",
        "origin": "https://engage.cloud.microsoft",
        "referer": (
            f"https://engage.cloud.microsoft/main/groups/{group_id}/all"
        ),
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/145.0.0.0 Safari/537.36"
        ),
        "x-request-id": request_id or str(uuid.uuid4()),
    }

    response = requests.post(_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Response was not valid JSON (status {response.status_code}): "
            f"{response.text[:500]}"
        ) from exc


def fetch_all_feed_pages(
    bearer_token: str,
    group_id: str,
    max_pages: int = 50,
    **kwargs,
) -> list:
    """Fetch all pages of group feed threads by following pagination cursors.

    Repeatedly calls :func:`fetch_feed_group_nested_clients`, extracting the
    next cursor from::

        response["data"]["feedGroup"]["feed"]["threads"]["pageInfo"]["endCursor"]

    Stops when the cursor is ``None`` or *max_pages* is reached.

    Args:
        bearer_token: OAuth2 Bearer token.
        group_id: Base64-encoded group ID.
        max_pages: Safety limit on the number of pages to fetch (default 50).
        **kwargs: Forwarded to :func:`fetch_feed_group_nested_clients`.

    Returns:
        List of raw API response dicts, one entry per page.
    """
    pages: list = []
    cursor: Optional[str] = None

    for page_num in range(1, max_pages + 1):
        print(f"Fetching page {page_num} (cursor={cursor!r})…")
        data = fetch_feed_group_nested_clients(
            bearer_token=bearer_token,
            group_id=group_id,
            older_than=cursor,
            **kwargs,
        )
        pages.append(data)

        try:
            threads_page_info = (
                data["data"]["feedGroup"]["feed"]["threads"]["pageInfo"]
            )
            cursor = threads_page_info.get("endCursor")
        except (KeyError, TypeError):
            cursor = None

        if not cursor:
            print("No more pages.")
            break

    return pages
