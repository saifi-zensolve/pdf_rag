import uuid

from fastapi import APIRouter

from src.rag.graph import main
from src.rag.graph.main import main as rag_main
from src.rag.model import ChatRequest, ChatResponse

SESSIONS: dict[str, list[dict]]

SESSIONS = {}

router = APIRouter(prefix="/api/v1")


@router.get("/llm")
async def invoke_gpt_example() -> dict:
    """Example endpoint to invoke GPT-4.1 Mini LLM and return its response."""
    from src.llm import GPT_4_1_Mini

    gpt_instance = GPT_4_1_Mini()
    response = gpt_instance.invoke_llm([{"role": "user", "content": "Hello, GPT-4.1 Mini!"}])

    return {"llm_response": response}


@router.get("/ask")
async def ask_question(question: str) -> dict:
    return rag_main(question=question)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid.uuid4())
    history = SESSIONS.get(session_id, [])

    result = rag_main({"question": request.question, "history": history})

    SESSIONS[session_id] = result["history"]

    return ChatResponse(answer=result["answer"], session_id=session_id, history=result["history"])


@router.get("/test")
async def test_endpoint() -> dict:
    main()
    return {"status": "ok"}
