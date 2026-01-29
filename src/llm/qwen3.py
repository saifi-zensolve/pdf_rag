from threading import Lock

from langchain_ollama import ChatOllama


class Qwen3:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton implementation to ensure only one instance of Qwen3 exists."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the Qwen3 model"""

        # Prevent re-initialization in singleton pattern
        if not hasattr(self, "_initialized"):
            self.model_name = "qwen3:8b"
            self.temperature = 0

            self.llm = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
            )

            self._initialized = True

    def invoke_llm(
        self,
        message: list[any],
        response_format: dict | None = None,
    ) -> any:
        """Invoke the LLM with a given message and optional response format.

        Args:
           message (list[any]): The message to send to the LLM.
           response_format (dict | None): The format of the LLM's response. Defaults to None.

        Returns:
           any: The LLM's response.
        """
        try:
            llm = self.llm

            if response_format:
                llm = llm.bind(format="json")

            response = llm.invoke(message)

            token_usage = response.response_metadata.get("token_usage", {})
            input_tokens = token_usage.get("input_tokens") or token_usage.get("prompt_tokens") or 0
            output_tokens = token_usage.get("output_tokens") or token_usage.get("completion_tokens") or 0
            total_tokens = token_usage.get("total_tokens", input_tokens + output_tokens)

            return {
                "message": response,
                "content": response.content,
                "usage": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": total_tokens,
                },
            }
        except Exception as e:
            raise RuntimeError(f"Failed to invoke LLM: {e}") from e
