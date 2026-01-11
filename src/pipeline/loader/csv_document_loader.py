import os

from langchain_community.document_loaders import CSVLoader, DirectoryLoader
from langchain_core.documents import Document


def load_csv_document(file_path: str) -> list[Document]:
    """Load all CSV files in a directory and convert them to LangChain Document objects. Add the source file name to each metadata key.

    Args:
        file_path (str): The path to the CSV file.
    Returns:
        list[Document]: A list of Document objects representing the CSV content.
    """
    if os.path.isdir(file_path):
        loader = DirectoryLoader(path=file_path, loader_cls=CSVLoader, glob="**/*.csv")
    elif os.path.isfile(file_path):
        if not file_path.endswith(".csv"):
            raise ValueError(f"File {file_path} is not a CSV file")

        loader = CSVLoader(file_path=file_path)
    else:
        raise FileNotFoundError(f"Path {file_path} does not exist")

    documents = loader.load()

    for document in documents:
        document.metadata["source_file"] = os.path.basename(document.metadata.get("source", ""))

    return documents
