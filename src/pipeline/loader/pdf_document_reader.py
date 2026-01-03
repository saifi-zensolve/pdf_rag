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
    if os.path.isdir(file_path):
        loader = DirectoryLoader(path=file_path, loader_cls=PyMuPDFLoader, glob="**/*.pdf")
    elif os.path.isfile(file_path):
        if not file_path.endswith(".pdf"):
            raise ValueError(f"File {file_path} is not a PDF file")

        loader = PyMuPDFLoader(file_path=file_path)
    else:
        raise FileNotFoundError(f"Path {file_path} does not exist")

    documents = loader.load()

    for document in documents:
        document.metadata["source_file"] = os.path.basename(document.metadata.get("source", ""))

    return documents
