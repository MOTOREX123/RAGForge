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

Answer the user's question using ONLY the provided context.

IMPORTANT RULES:

1. Answer the question directly.
2. Use only information supported by the provided context.

IMPORTANT ENTITY MATCHING RULE:

Every factual claim must refer to the exact concept asked about.

Do not transfer a property, definition, advantage, disadvantage,
algorithm characteristic, or other statement from one concept to another
just because it appears in the context.

For example, if the question asks about Depth-First Search and the context
also contains information about Best-First Search, Iterative Deepening DFS,
or Breadth-First Search, do not attribute those properties to Depth-First
Search unless the context explicitly says they apply to Depth-First Search.

When multiple related algorithms or concepts appear in the context,
carefully distinguish them before answering.

If a retrieved section describes a different concept, ignore that section
for the answer.

3. Do not invent facts.
4. Cover all important parts of the question.
5. Keep the answer concise but complete.
6. Organize multi-part answers into short paragraphs or bullet points when useful.
7. Each context section has a citation number such as [1], [2], [3].
8. Cite factual claims using the relevant citation number.
9. Only use citation numbers that actually appear in the context.
10. Do not create or guess citation numbers.
11. If the context does not contain enough information, say:
"The provided documents do not contain enough information to answer this."

CONTRASTING CONCEPTS RULE:

When the context explicitly contrasts two related concepts, keep their
definitions and properties separate.

If the question asks about one side of a contrast, use only the information
that belongs to that concept.

For example, if the context contrasts underfitting and overfitting:
- Underfitting refers to a model that is too simple and cannot capture
  important variation in the data.
- Overfitting refers to a model that fits the training data too closely
  and does not generalize well.

Do not assign the definition or characteristics of one concept to the other.

Before finalizing the answer, check that every definition or characteristic
belongs to the exact concept asked about.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    try:
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
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 512
                }
            },
            timeout=180
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Ollama request failed: {e}")

        if hasattr(e, "response") and e.response is not None:
            print(f"Ollama response: {e.response.text}")

        raise

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

1. Answer the question directly and clearly.
2. Do not use or mention the user's local documents.
3. Do not create citations.
4. Do not invent information.
5. If you are uncertain, clearly say so.
6. Keep the answer concise unless more detail is useful.



USER QUESTION:
{question}

ANSWER:
"""

    try:
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
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 512
                }
            },
            timeout=180
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Ollama request failed: {e}")

        if hasattr(e, "response") and e.response is not None:
            print(f"Ollama response: {e.response.text}")

        raise

    data = response.json()

    return data["message"]["content"]