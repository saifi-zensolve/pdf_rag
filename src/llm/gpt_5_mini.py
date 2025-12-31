import os
from threading import Lock

from langchain_openai import ChatOpenAI


class GPT_5_Mini:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton implementation to ensure only one instance of GPT_5_Mini exists."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the GPT-5 Mini model."""

        # Prevent re-initialization in singleton pattern
        if not hasattr(self, "_initialized"):
            self.model_name = "gpt-5-mini"
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.temperature = 0

            self.llm = ChatOpenAI(
                model_name=self.model_name,
                openai_api_key=self.api_key,
                temperature=self.temperature,
            )

            self._initialized = True

    def invoke_llm(self, message: list[any]) -> any:
        """Invoke the LLM with the provided message."""
        try:
            raise NotImplementedError("GPT-5 Mini model is not yet implemented.")
        except Exception as e:
            raise RuntimeError(f"Failed to invoke LLM: {e}") from e
