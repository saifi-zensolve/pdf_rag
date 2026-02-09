from typing import TypedDict

from langchain_core.documents import Document

from src.rag.intent.classifier import Intent


class State(TypedDict, total=False):
    """Type definition for the state of the chatbot.

    Args:
        question (str): The user's input question to the chatbot.
        docs (list[Document]): A list of documents to be used by the chatbot.
        filtered_docs (list[Document]): A list of filtered documents based on the user's input question.
        prompt (str): The prompt for the chatbot.
        answer (str): The response from the chatbot.
        history (list[dict[str, str]]): A list of previous user inputs and chatbot responses in the form of a dictionary.
        error (str): An error message if an exception occurs during the chatbot's execution.
        intent (Intent): The intent of the user's input.
        intent_confidence (float): The confidence level of the intent of the user's input.
    """

    question: str
    docs: list[Document]
    filtered_docs: list[Document]
    prompt: str
    answer: str
    history: list[dict[str, str]]
    error: str
    intent: Intent
    intent_confidence: float
