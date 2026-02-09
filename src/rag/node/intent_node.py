from src.rag.intent.classifier import IntentClassifier
from src.rag.state import State


def classify_intent(state: State) -> State:
    result = IntentClassifier().classify(question=state["question"])
    return {**state, "intent": result.intent, "intent_confidence": result.confidence}
