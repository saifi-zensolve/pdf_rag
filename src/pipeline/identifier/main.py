import hashlib
import os


def generate_id(text: str) -> str:
    """Generate a deterministic id for the given text.

    Args:
        text (str): The text to generate an id for.
    Returns:
        id (str): A deterministic id for the given text.
    """
    return hashlib.md5(text.encode()).hexdigest()


def generate_chunk_id(source: str, page: str, chunk_idx: str, version: str, text: str) -> str:
    """Generate a deterministic id for the given chunk.

    Args:
        source (str): The name of the source of the chunk.
        page (str): The name of the page.
        chunk_idx (str): The index of the chunk
        version (str): The version of the chunk.
        text (str): The text of the chunk.
    Returns:
       id (str): A deterministic id for the given chunk.
    """
    source = os.path.basename(source or "")
    page = page if page is not None else -1

    raw = f"{source}-{page}-{chunk_idx}-{version}-{text}".encode()

    return hashlib.md5(raw).hexdigest()
