import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma3:4b"


def generate_ollama_answer(
    question: str,
    context: str
) -> str:
    """
    Generate an answer using Ollama with retrieved document context.
    """

    prompt = f"""
You are an AI assistant inside a Retrieval-Augmented Generation system.

Answer the user's question using the provided context.

IMPORTANT RULES:

1. Use ONLY the provided context to answer the question.
2. Do not invent information that is not supported by the context.
3. If the context does not contain enough information, clearly say:
   "The provided documents do not contain enough information to answer this."
4. Each context section has a citation number such as [1], [2], [3].
5. When making a factual claim, cite the relevant context number.
6. Put citations directly after the claim, for example:
   "Overfitting occurs when a model learns the training data too closely. [1]"
7. Only use citation numbers that actually appear in the provided context.
8. Do not create or guess citation numbers.
9. Give a clear and concise answer.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


def generate_general_answer(question: str) -> str:
    """
    Generate an answer using Ollama without document retrieval.
    """

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using your general knowledge.

IMPORTANT RULES:

1. Answer the user's question directly and clearly.
2. Do not use or mention the user's local documents.
3. Do not create citations.
4. If you are uncertain, clearly say so.
5. Keep the answer concise unless more detail is useful.

USER QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]