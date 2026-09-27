import re

from utils.retriever import retrieve_chunks


# ============================================================
# WEB INTENT
# ============================================================

WEB_KEYWORDS = [
    "latest",
    "current",
    "today",
    "now",
    "recent",
    "recently",
    "news",
    "this week",
    "this month",
    "this year",
    "updated",
    "update",
    "price",
    "weather",
    "stock",
    "release",
    "new version",
]


def is_web_query(question: str) -> bool:
    """
    Detect questions that clearly request
    current or time-sensitive information.

    Uses word/phrase matching instead of raw substring matching.
    """

    question_lower = question.lower().strip()

    for keyword in WEB_KEYWORDS:

        # Multi-word phrases
        if " " in keyword:
            if keyword in question_lower:
                return True

        # Single words
        else:
            pattern = rf"\b{re.escape(keyword)}\b"

            if re.search(pattern, question_lower):
                return True

    return False


# ============================================================
# ROUTER
# ============================================================

def route_query(
    vector_db,
    question: str,
    k: int = 5,
    threshold: float = 0.65
):
    """
    Route a question to:

    - local  -> relevant information exists in local documents
    - web    -> question clearly requires current information
    - general -> neither local nor web-specific
    """

    # ---------------------------------------------------------
    # STEP 1: Explicit web intent
    # ---------------------------------------------------------

    if is_web_query(question):

        return {
            "source": "web",
            "results": [],
            "reason": "time-sensitive query"
        }

    # ---------------------------------------------------------
    # STEP 2: Search local documents
    # ---------------------------------------------------------

    results = retrieve_chunks(
        vector_db,
        question,
        k=k,
        threshold=threshold
    )

    # ---------------------------------------------------------
    # STEP 3: Relevant local information found
    # ---------------------------------------------------------

    if results:

        return {
            "source": "local",
            "results": results,
            "reason": "relevant local documents found"
        }

    # ---------------------------------------------------------
    # STEP 4: No local information and no web intent
    # ---------------------------------------------------------

    return {
        "source": "general",
        "results": [],
        "reason": "no sufficiently relevant local information"
    }