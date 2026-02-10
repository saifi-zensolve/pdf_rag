from src.rag.intent.classifier import CONFIDENCE_THRESHOLD, Intent
from src.rag.node.gate import hard_gate
from src.rag.node.intent_node import classify_intent
from src.rag.state import State

ROUTING_TABLE = {
    Intent.CLAIM_STATUS: "SQL",
    Intent.ACTIVE_POLICIES_COUNT: "SQL",
    Intent.PENDING_CLAIMS: "SQL",
    Intent.POLICY_STATUS: "SQL",
    Intent.UNKNOWN: "VECTOR",
}


def route_by_intent(state: State) -> str:
    if state["intent_confidence"] < CONFIDENCE_THRESHOLD:
        return "fallback"
    intent = state["intent"]

    if intent == Intent.CLAIM_STATUS:
        return "claim_status"
    elif intent == Intent.ACTIVE_POLICIES_COUNT:
        return "active_policies_count"
    elif intent == Intent.PENDING_CLAIMS:
        return "pending_claims"
    elif intent == Intent.POLICY_STATUS:
        return "policy_status"


def route_question(question: str):
    if not hard_gate(question):
        return "REJECT"

    intent, _ = classify_intent(question)

    if intent == Intent.UNKNOWN:
        return "REJECT"

    return ROUTING_TABLE.get(intent, "REJECT")
