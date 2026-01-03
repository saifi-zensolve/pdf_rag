import os
from collections import defaultdict

from src.pipeline.config import EMBEDDING_DIMENSION, EMBEDDING_VERSION
from src.pipeline.embedding import get_embeddings
from src.pipeline.identifier import generate_chunk_id
from src.pipeline.loader import load_pdf_document
from src.pipeline.splitter import split_documents
from src.pipeline.store import get_store


def ingest_pipeline(path: str) -> dict:
    """Ingest a PDF document and store its embeddings.

    Args:
        path (str): The path to the PDF document
    Returns:
        dict: A dictionary containing the status of the ingestion process.
    """
    # Step 1: Load the PDF documents
    documents = load_pdf_document(path)

    # Step 2: Chunk the text into smaller chunks (e.g., sentences)
    chunks = split_documents(documents)

    # Step 3: Embed each chunk using a vector store embedding model
    embeddings = get_embeddings(embedding_provider="free-slow")

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    # Step 4: Generate deterministic ids for each chunk
    hash_ids = []
    doc_counter = defaultdict(int)

    for chunk in chunks:
        source = chunk.metadata.get("source_file")
        page = chunk.metadata.get("page", -1)

        # Per-document Indexing: Support avoiding changes to any document when some other document get changed
        idx = doc_counter[source]
        doc_counter[source] += 1

        # (Optional) File Fingerprint: Generate a unique identifier for each file to avoid re-embedding a file (yet to implement)
        chunk.metadata["embedding_version"] = EMBEDDING_VERSION
        chunk.metadata["filename"] = os.path.basename(source or "")

        chunk_id = generate_chunk_id(
            source=source,
            page=page,
            chunk_idx=idx,
            version=EMBEDDING_VERSION,
            text=chunk.page_content,
        )
        chunk.metadata["chunk_id"] = chunk_id

        hash_ids.append(chunk_id)

    # Step 5: Store the embeddings and metadata in the vector store
    store = get_store(embedding=embeddings, store_type="qdrant", dimensions=EMBEDDING_DIMENSION)
    store.add_texts(texts, metadatas, ids=hash_ids)

    return {"status": "success", "path": path}
