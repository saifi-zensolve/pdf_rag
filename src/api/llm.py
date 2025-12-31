import os

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/llm")
async def invoke_gpt_example() -> dict:
    """Example endpoint to invoke GPT-4.1 Mini LLM and return its response."""
    from src.llm import GPT_4_1_Mini

    gpt_instance = GPT_4_1_Mini()
    response = gpt_instance.invoke_llm([{"role": "user", "content": "Hello, GPT-4.1 Mini!"}])

    return {"llm_response": response}


@router.get("/test")
async def test_endpoint() -> dict:
    from src.data import load_pdf_document
    from src.embedding import get_embeddings
    from src.store import get_store

    path = os.getenv("DOCUMENTS_PATH", "./documents")
    documents = load_pdf_document(path)
    documents = documents[:10]  # Limit to first 10 documents for testing

    embeddings = get_embeddings(embedding_provider="free")  # Just to test embedding loading
    store = get_store(embedding=embeddings)
    store.add_documents(documents)

    result = store.similarity_search("What is Renters Insurance?", k=3)

    return {"results": [{"content": r.page_content, "metadata": r.metadata} for r in result]}
