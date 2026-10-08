import os
import requests

from config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENROUTER_MODEL = "meta-llama/llama-3.1-8b-instruct"


def _get_openrouter_model() -> str:
    return os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL)


def generate_openrouter_answer(
    question: str,
    context: str | None = None
) -> tuple[str, str]:
    """
    Generate an answer using OpenRouter.

    Args:
        question: The user's question.
        context: Optional retrieved document context for grounded answers.

    Returns:
        Tuple of (answer, model_name_used)
    """
    if not OPENROUTER_API_KEY or not OPENROUTER_API_KEY.strip():
        raise ValueError("OPENROUTER_API_KEY is not set")

    model = _get_openrouter_model()

    if context:
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

SCOPE CONTROL RULE:

If the user asks for a specific number of items (for example, "one limitation"),
provide only that number. When multiple valid facts are present in the context,
choose the fact that most directly answers the user's requested scope.
Do not list multiple alternatives unless the user asks for them.
Never use the position/order of a fact in the context as the reason to prefer it.
Continue following the existing entity-matching and source-grounding rules.

CITATION RULES:

1. Each context section has a citation number such as [1], [2], [3].
2. Every factual claim must cite the citation number of the context section that directly contains the evidence supporting that exact claim.
3. Do NOT cite a section merely because it discusses the same general topic.
4. Do NOT use a citation number from a related or nearby concept when the specific fact is found in another section.
5. Only use citation numbers that actually appear in the provided context.
6. Never create, guess, or change citation numbers.
7. If a claim is not supported by the provided context, do not cite an unrelated section as support for it.

3. Do not invent facts.
4. Cover all important parts of the question.
5. Keep the answer concise but complete.
6. Organize multi-part answers into short paragraphs or bullet points when useful.
7. If the context does not contain enough information, say:
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
    else:
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
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY.strip()}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 512
            },
            timeout=120
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(f"OpenRouter request failed: {e}")

        if hasattr(e, "response") and e.response is not None:
            print(f"OpenRouter response: {e.response.text}")

        raise

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    used_model = data.get("model", model)

    return answer, used_model