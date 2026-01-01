from fastapi import APIRouter

from src.app import call_rag as rag

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
    return rag()
