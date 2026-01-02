import os

from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_core.documents import Document


def load_pdf_document(file_path: str) -> list[Document]:
    """Load all PDF files in a directory and convert them to LangChain Document objects. Add the source file name to each metadata key.

    Args:
        file_path (str): The path to the PDF file.
    Returns:
        list[Document]: A list of Document objects representing the PDF content.
    """
    loader = DirectoryLoader(path=file_path, loader_cls=PyMuPDFLoader, glob="**/*.pdf")
    documents = loader.load()

    for document in documents:
        document.metadata["source_file"] = os.path.basename(document.metadata.get("source", ""))

    return documents
