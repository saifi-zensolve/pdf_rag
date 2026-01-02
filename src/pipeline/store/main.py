from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


def get_store(
    embedding: Embeddings, store_type: str = "memory", dimensions: int = 0
) -> VectorStore:
    """Get a vector store based on the specified provider.
    Args:
        provider (str): The name of the provider to use. Supported values are 'memory' and 'qdrant'.
    Returns:
        VectorStore: An instance of the selected VectorStore class.
    """
    if store_type == "memory":
        return InMemoryVectorStore(embedding=embedding)
    elif store_type == "qdrant":
        client = QdrantClient(path="./data_store/qdrant.qdrant")
        collections = [c.name for c in client.get_collections().collections]
        if "docs" not in collections:
            client.create_collection(
                collection_name="docs",
                vectors_config=VectorParams(size=dimensions, distance=Distance.COSINE),
            )
        return QdrantVectorStore(client=client, collection_name="docs", embedding=embedding)
    else:
        raise RuntimeError(f"Unsupported store type: {store_type}")
