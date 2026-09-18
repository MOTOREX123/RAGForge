from google import genai
from google.genai import types

from config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def web_search(question: str) -> dict:
    """
    Search the web using Gemini Google Search grounding.

    Returns:
        {
            "answer": str,
            "sources": list[dict],
            "search_queries": list[str]
        }
    """

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=config
    )

    answer = response.text

    sources = []
    search_queries = []

    # Get grounding metadata
    if response.candidates:

        candidate = response.candidates[0]

        metadata = candidate.grounding_metadata

        if metadata:

            # Search queries Gemini used
            if metadata.web_search_queries:
                search_queries = list(
                    metadata.web_search_queries
                )

            # Sources returned by Google Search
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
        "search_queries": search_queries
    }