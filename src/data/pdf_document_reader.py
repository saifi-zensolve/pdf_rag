from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_core.documents import Document


def load_pdf_document(file_path: str) -> list[Document]:
    """Load a PDF document and return its content as a list of Document objects.
    Args:
        file_path (str): The path to the PDF file.
    Returns:
        list[Document]: A list of Document objects representing the PDF content.
    """
    loader = DirectoryLoader(path=file_path, loader_cls=PyMuPDFLoader, glob="**/*.pdf")
    documents = loader.load()
    return documents
