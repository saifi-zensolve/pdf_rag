import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_core.documents import Document
from tqdm import tqdm

from src.logger import init_logger
from src.pipeline.config import EMBEDDING_DIMENSION, EMBEDDING_VERSION
from src.pipeline.embedding import get_embeddings
from src.pipeline.identifier import generate_chunk_id
from src.pipeline.loader import load_csv_document, load_pdf_document
from src.pipeline.splitter import split_documents
from src.pipeline.store import get_store

logger = init_logger(__name__)


def __load_all_documents(path: str) -> dict:
    """Load all documents from a given path.

    Args:
       path (str): The path to the directory where the documents are stored.
    Returns:
       list[dict]: A list of dictionaries, where each dictionary represents a document and contains information about its metadata.
    """
    pdf_documents = load_pdf_document(path)
    csv_documents = load_csv_document(path)

    documents = pdf_documents + csv_documents

    return documents


def __process_chunks(chunks: list[Document]) -> None:
    chunk_batches = list(create_batch(chunks=chunks))

    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(thread_worker, chunk_batch) for chunk_batch in chunk_batches]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Embedded and Store: "):
            pass


def thread_worker(chunk_batch: list[Document]) -> None:
    # Step 3: Embed each chunk using a vector store embedding model
    embedder = get_embeddings(embedding_provider="free-slow")
    store = get_store(embedding=embedder, store_type="qdrant", dimensions=EMBEDDING_DIMENSION)

    texts = [chunk.page_content for chunk in chunk_batch]
    metadatas = [chunk.metadata for chunk in chunk_batch]

    # Step 4: Generate deterministic ids for each chunk
    hash_ids = []
    doc_counter = defaultdict(int)

    for chunk in chunk_batch:
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
    store.add_texts(texts, metadatas, ids=hash_ids)


def create_batch(chunks: list[Document], size: int = 96):
    for i in range(0, len(chunks), size):
        yield chunks[i : i + size]


def ingest_pipeline(path: str) -> dict:
    """Ingest a PDF document and store its embeddings.

    Args:
        path (str): The path to the PDF document
    Returns:
        dict: A dictionary containing the status of the ingestion process.
    """
    logger.info(f"Loading documents from {path}")
    # Step 1: Load the documents
    documents = __load_all_documents(path=path)
    logger.info(f"Found {len(documents)} documents")

    logger.info("Splitting documents into smaller chunks")
    # Step 2: Chunk the text into smaller chunks (e.g., sentences)
    chunks = split_documents(documents)
    logger.info(f"Found {len(chunks)} chunks")

    __process_chunks(chunks=chunks)

    return {"status": "success", "path": path}
