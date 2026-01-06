from typing import TypedDict

from langchain_core.documents import Document
from langgraph.graph import StateGraph

from src.llm.gpt_41_mini import GPT_4_1_Mini
from src.pipeline.embedding import get_embeddings
from src.pipeline.store import get_store
from src.rag.model import ChatRequest


class State(TypedDict):
    question: str
    docs: list[Document]
    filtered_docs: list[Document]
    prompt: str
    answer: str


embeddings = get_embeddings("free-slow")
retriever = get_store(embedding=embeddings, store_type="qdrant", dimensions=768).as_retriever(k=3)


def retrieve_node(state: State):
    docs = retriever.invoke(state["question"])
    return {"docs": docs}


def pre_guardrail_node(state: State):
    """
    This node is responsible for cleaning the documents before passing them to the next node.
    It ensures that each document is unique by hashing its text content. This ensures that
    the same document is not passed to multiple nodes, which can lead to duplicate results.
    This is important because the LLM may return the same response for different documents,
    and we want to avoid duplicate results.

    Args:
        state (State): The state of graph node.
    """
    cleaned_docs = []
    seen = set()

    for document in state["docs"]:
        text = (document.page_content or "").strip()

        if not text:
            continue

        key = hash(text)

        if key in seen:
            continue

        seen.add(key)
        cleaned_docs.append(document)

    return {"filtered_docs": cleaned_docs}


def prompt_node(state: State):
    context = "\n\n---\n\n".join(document.page_content for document in state["filtered_docs"])

    prompt = f"""
You are a helpful insurance expert.
Answer the question using ONLY the context below.

CONTEXT:
{context}

QUESTION:
{state["question"]}
"""
    print(f"prompt: {prompt}")
    return {"prompt": prompt}


def llm_node(state: State):
    response = GPT_4_1_Mini().invoke_llm(state["prompt"])
    return {"answer": response["content"]}


def post_guardrail_node(state: State):
    answer = state["answer"].lower()
    if "based on the provided documents" not in answer and "i don't know" in answer:
        return state

    return {"answer": state["answer"]}


def main(request: ChatRequest) -> dict:
    graph = StateGraph(State)

    graph.add_node("retrieve_node", retrieve_node)
    graph.add_node("pre_guardrail_node", pre_guardrail_node)
    graph.add_node("prompt_node", prompt_node)
    graph.add_node("llm_node", llm_node)
    graph.add_node("post_guardrail_node", post_guardrail_node)

    graph.set_entry_point("retrieve_node")
    graph.add_edge("retrieve_node", "pre_guardrail_node")
    graph.add_edge("pre_guardrail_node", "prompt_node")
    graph.add_edge("prompt_node", "llm_node")
    graph.add_edge("llm_node", "post_guardrail_node")

    app = graph.compile()

    response = app.invoke({"question": request["question"]})

    return {
        "status": "success",
        "question": request["question"],
        "answer": response["answer"],
        "history": [],
    }
