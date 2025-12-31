from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from qdrant_client import QdrantClient


def get_store(embedding: Embeddings, store_type: str = "memory") -> VectorStore:
    """Get a vector store based on the specified provider.
    Args:
        provider (str): The name of the provider to use. Supported values are 'memory' and 'qdrant'.
    Returns:
        VectorStore: An instance of the selected VectorStore class.
    """
    if store_type == "memory":
        return InMemoryVectorStore(embedding=embedding)
    elif store_type == "qdrant":
        return QdrantClient(path="./data_store/qdrant.qdrant")
    else:
        raise RuntimeError(f"Unsupported store type: {store_type}")
