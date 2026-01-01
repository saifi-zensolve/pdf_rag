import hashlib
import os

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.data import load_pdf_document
from src.embedding import get_embeddings
from src.store import get_store


def __split_documents(documents: list[Document]) -> list[Document]:
    """Split a list of documents into smaller chunks (e.g., sentences).

    Args:
        documents (list[Document]): A list of langchain.Document objects.
    Returns:
        chunks (list[Document]): A list of langchain.Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, add_start_index=True
    )
    chunks = splitter.split_documents(documents)
    print(f"From {len(documents)} documents to {len(chunks)} chunks")
    return chunks


def __generate_id(text: str) -> str:
    """Generate a deterministic id for the given text.

    Args:
        text (str): The text to generate an id for.
    Returns:
        id (str): A deterministic id for the given text.
    """
    return hashlib.md5(text.encode()).hexdigest()


def call_rag() -> dict:
    # Step 1: Load the PDF documents
    path = os.getenv("DOCUMENTS_PATH", "./documents")
    documents = load_pdf_document(path)

    # Step 2: Chunk the text into smaller chunks (e.g., sentences)
    chunks = __split_documents(documents)

    # Step 3: Embed each chunk using a vector store embedding model
    embeddings = get_embeddings(embedding_provider="free-slow")

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    # vectors = embeddings.embed_documents(texts)

    # Step 4: Generate deterministic ids for each chunk
    hash_ids = [__generate_id(text) for text in texts]

    # Step 5: Store the embeddings and metadata in the vector store
    store = get_store(embedding=embeddings, store_type="qdrant", dimensions=768)
    store.add_texts(texts, metadatas, ids=hash_ids)

    result = store.similarity_search("What is Renters Insurance?", k=3)

    return {"response": result}
