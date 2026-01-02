import os

from langchain_core.embeddings import Embeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


def get_embeddings(embedding_provider: str = "free") -> Embeddings:
    """Get embeddings based on the specified provider.
    Args:
        provider (str): The name of the provider to use. Supported values are 'free', 'free-slow', and 'openai'.
    Returns:
        Embeddings: An instance of the selected Embeddings class.
    """
    if embedding_provider == "free":
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    elif embedding_provider == "free-slow":
        return HuggingFaceEmbeddings(
            model_name=os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-mpnet-base-v2")
        )
    elif embedding_provider == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-small")
    else:
        raise RuntimeError(f"Unsupported embedding provider: {embedding_provider}")
