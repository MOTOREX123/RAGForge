import requests

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, OPENROUTER_API_KEY


# ============================================================
# GEMINI CLIENT
# ============================================================

gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ============================================================
# OPENROUTER SETTINGS
# ============================================================

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# You can change this later.
OPENROUTER_MODEL = "openrouter/free"


# ============================================================
# GEMINI WEB SEARCH
# ============================================================

def search_with_gemini(question: str) -> dict:
    """
    Search the web using Gemini Google Search grounding.
    """

    if not gemini_client:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    response = gemini_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=config
    )

    answer = response.text

    sources = []
    search_queries = []

    if response.candidates:

        candidate = response.candidates[0]

        metadata = candidate.grounding_metadata

        if metadata:

            if metadata.web_search_queries:
                search_queries = list(
                    metadata.web_search_queries
                )

            if metadata.grounding_chunks:

                for chunk in metadata.grounding_chunks:

                    if chunk.web:

                        sources.append({
                            "title": chunk.web.title,
                            "url": chunk.web.uri
                        })

    return {
        "answer": answer,
        "sources": sources,
        "search_queries": search_queries,
        "provider": "Gemini"
    }


# ============================================================
# OPENROUTER WEB SEARCH
# ============================================================

def search_with_openrouter(question: str) -> dict:
    """
    Search the web using OpenRouter's web-search tool.

    For current/latest questions, explicitly request fresh
    information and prioritize authoritative sources.
    """

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured."
        )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "RAGForge"
    }

    # Detect freshness-sensitive questions
    current_keywords = [
        "latest",
        "current",
        "today",
        "now",
        "recent",
        "recently",
        "newest",
        "updated",
        "this week",
        "this month",
        "this year"
    ]

    question_lower = question.lower()

    is_current_query = any(
        keyword in question_lower
        for keyword in current_keywords
    )

    if is_current_query:

        search_instruction = f"""
You are answering a CURRENT/TIME-SENSITIVE web question.

User question:
{question}

IMPORTANT:

1. Search the web before answering.
2. Use information that is current as of October 2, 2026.
3. Do NOT rely on old model knowledge.
4. Prefer official/primary sources whenever available.
5. For software versions, releases, APIs, libraries, frameworks,
   or technical specifications, prefer the project's official website,
   official documentation, or official release announcement.
6. Verify that the source actually describes the latest release.
7. Pay attention to the publication/release date.
8. Do not answer with an older version merely because it appears
   prominently in search results.
9. If multiple recent sources disagree, investigate further before
   answering.
10. State the exact version and release date when available.
11. Provide URLs/citations for the sources used.

Give a concise answer followed by the relevant sources.
"""

    else:

        search_instruction = f"""
Answer the following question using web search:

{question}

Use authoritative sources when possible.
Provide citations/sources for factual claims.
"""

    payload = {
        "model": OPENROUTER_MODEL,

        "tools": [
            {
                "type": "openrouter:web_search"
            }
        ],

        "messages": [
            {
                "role": "user",
                "content": search_instruction
            }
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    choices = data.get("choices", [])

    if not choices:
        raise RuntimeError(
            "OpenRouter returned no choices."
        )

    message = choices[0].get("message", {})

    answer = message.get("content", "")

    # ========================================================
    # EXTRACT SOURCES ACTUALLY USED IN THE ANSWER
    # ========================================================

    import re

    sources = []

    # --------------------------------------------------------
    # Build a lookup from OpenRouter annotations
    # --------------------------------------------------------

    annotation_sources = {}

    annotations = message.get("annotations", [])

    for annotation in annotations:

        if annotation.get("type") != "url_citation":
            continue

        citation = annotation.get(
            "url_citation",
            {}
        )

        url = citation.get("url")

        if not url:
            continue

        title = citation.get("title") or url

        normalized_url = url.rstrip("/").lower()

        annotation_sources[normalized_url] = {
            "title": title.strip(),
            "url": url
        }

    # --------------------------------------------------------
    # Extract URLs actually appearing in the answer
    # --------------------------------------------------------

    url_pattern = r"https?://[^\s<>\])}\"']+"

    answer_urls = re.findall(
        url_pattern,
        answer
    )

    # --------------------------------------------------------
    # Remove duplicates while preserving answer order
    # --------------------------------------------------------

    seen_urls = set()

    for url in answer_urls:

        # Remove punctuation that may follow a URL
        url = url.rstrip(".,;:!?)]}")

        normalized_url = url.rstrip("/").lower()

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)

        # Prefer the title supplied by OpenRouter
        if normalized_url in annotation_sources:

            source = annotation_sources[normalized_url]

            sources.append({
                "title": source["title"],
                "url": source["url"]
            })

        else:

            # URL was explicitly included in the answer,
            # but OpenRouter did not provide a title.
            sources.append({
                "title": url,
                "url": url
            })

        if len(sources) >= 8:
            break

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------
    #
    # If the answer contains no URLs, use annotations.
    # This prevents the source list from becoming empty when
    # the model cites sources through structured annotations.
    # --------------------------------------------------------

    if not sources:

        seen_urls = set()
        seen_titles = set()

        for source in annotation_sources.values():

            normalized_url = source["url"].rstrip("/").lower()
            normalized_title = source["title"].strip().lower()

            if normalized_url in seen_urls:
                continue

            if normalized_title in seen_titles:
                continue

            seen_urls.add(normalized_url)
            seen_titles.add(normalized_title)

            sources.append({
                "title": source["title"],
                "url": source["url"]
            })

            if len(sources) >= 8:
                break

    return {
        "answer": answer,
        "sources": sources,
        "search_queries": [],
        "provider": "OpenRouter"
    }
# ============================================================
# MAIN WEB SEARCH WITH FALLBACK
# ============================================================

def web_search(question: str) -> dict:
    """
    Search the web.

    Primary:
        Gemini Google Search

    Fallback:
        OpenRouter web search

    If Gemini quota is exhausted or unavailable,
    automatically use OpenRouter.
    """

    # --------------------------------------------------------
    # TRY GEMINI FIRST
    # --------------------------------------------------------

    try:

        print("\nWeb search provider: Gemini")

        return search_with_gemini(question)

    except Exception as gemini_error:

        print(
            f"\nGemini web search failed: {gemini_error}"
        )

        print(
            "Falling back to OpenRouter web search..."
        )

    # --------------------------------------------------------
    # FALLBACK TO OPENROUTER
    # --------------------------------------------------------

    try:

        result = search_with_openrouter(question)

        print(
            "Web search provider: OpenRouter"
        )

        return result

    except Exception as openrouter_error:

        print(
            f"\nOpenRouter web search failed: "
            f"{openrouter_error}"
        )

        # ----------------------------------------------------
        # BOTH WEB PROVIDERS FAILED
        # ----------------------------------------------------

        return {
            "answer": (
                "I could not access the web right now. "
                "Gemini and OpenRouter web search both failed."
            ),
            "sources": [],
            "search_queries": [],
            "provider": "none"
        }