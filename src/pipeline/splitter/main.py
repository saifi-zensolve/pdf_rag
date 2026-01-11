from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[Document]) -> list[Document]:
    """Split a list of documents into smaller chunks (e.g., sentences).

    Args:
        documents (list[Document]): A list of langchain.Document objects.
    Returns:
        chunks (list[Document]): A list of langchain.Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120, add_start_index=True)
    chunks = splitter.split_documents(documents)
    print(f"From {len(documents)} documents to {len(chunks)} chunks")
    return chunks
