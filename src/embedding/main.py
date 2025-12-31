from langchain_core.embeddings import Embeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


def get_embeddings(provider: str = "free") -> Embeddings:
    """Get embeddings based on the specified provider.
    Args:
        provider (str): The embedding provider to use. Options are "free" or "openai". Default is "free".
    Returns:
        Embeddings: An instance of the selected Embeddings class.
    """
    if provider == "free":
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    elif provider == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-small")
    else:
        raise RuntimeError(f"Unsupported embedding provider: {provider}")
