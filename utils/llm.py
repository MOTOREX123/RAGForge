from google import genai

from config import GEMINI_API_KEY


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please add it to the .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(
    question: str,
    retrieved_chunks: list[dict]
) -> str:
    """
    Generate an answer using Gemini based only
    on the retrieved document context.
    """

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
Source: {chunk['source']}
Page: {chunk['page']}
Chunk ID: {chunk['chunk_id']}
Similarity Score: {chunk['score']:.4f}

Content:
{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. If the answer cannot be found in the context, say:
   "I could not find this information in the provided documents."
3. Give a clear and concise answer.
4. Do not mention that you are an AI unless necessary.
5. At the end, provide the source pages used.

USER QUESTION:
{question}

RETRIEVED CONTEXT:
{context}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text