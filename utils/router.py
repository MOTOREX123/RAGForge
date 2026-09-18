from utils.retriever import retrieve_chunks


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
    "2026",
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
    Detect questions that are likely to require
    current or real-time web information.
    """

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in WEB_KEYWORDS
    )


def route_query(
    vector_db,
    question: str,
    k: int = 5,
    threshold: float = 0.65
):
    """
    Route a question to either:
    - local document retrieval
    - web retrieval
    - general Ollama
    """

    # -------------------------------------------------
    # STEP 1: Check whether the question needs the web
    # -------------------------------------------------

    if is_web_query(question):

        return {
            "source": "web",
            "results": [],
            "reason": "time-sensitive query"
        }

    # -------------------------------------------------
    # STEP 2: Search local documents
    # -------------------------------------------------

    results = retrieve_chunks(
        vector_db,
        question,
        k=k,
        threshold=threshold
    )

    # -------------------------------------------------
    # STEP 3: If relevant local information exists
    # -------------------------------------------------

    if results:

        return {
            "source": "local",
            "results": results,
            "reason": "relevant local documents found"
        }

    # -------------------------------------------------
    # STEP 4: Otherwise use web
    # -------------------------------------------------

    return {
    "source": "general",
    "results": [],
    "reason": "no sufficiently relevant local information"
}