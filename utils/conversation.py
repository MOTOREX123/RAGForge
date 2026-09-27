from collections import defaultdict
from threading import Lock


class ConversationMemory:
    """
    Simple in-memory conversation history for the RAG API.

    Stores recent user/assistant turns per conversation_id.
    This is intentionally lightweight for the current project.
    """

    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self._conversations = defaultdict(list)
        self._lock = Lock()

    def add_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_message: str,
    ) -> None:
        """
        Store one completed conversation turn.
        """

        with self._lock:
            history = self._conversations[conversation_id]

            history.append({
                "user": user_message,
                "assistant": assistant_message,
            })

            # Keep only the most recent turns.
            self._conversations[conversation_id] = history[
                -self.max_turns:
            ]

    def get_history(
        self,
        conversation_id: str,
    ) -> list[dict]:
        """
        Return the conversation history.
        """

        with self._lock:
            return list(
                self._conversations.get(
                    conversation_id,
                    []
                )
            )

    def clear(
        self,
        conversation_id: str,
    ) -> None:
        """
        Delete one conversation.
        """

        with self._lock:
            self._conversations.pop(
                conversation_id,
                None
            )