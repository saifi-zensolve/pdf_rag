import json
from enum import Enum
from typing import NamedTuple

from src.llm.qwen3 import Qwen3


class Intent(Enum):
    CLAIM_STATUS = "CLAIM_STATUS"
    POLICY_STATUS = "POLICY_STATUS"
    ACTIVE_POLICIES_COUNT = "ACTIVE_POLICIES_COUNT"
    PENDING_CLAIMS = "PENDING_CLAIMS"
    UNKNOWN = "UNKOWN"


class IntentResult(NamedTuple):
    intent: Intent
    confidence: float


ALLOWED_INTENTS = {i.value for i in Intent if i != Intent.UNKNOWN}
CONFIDENCE_THRESHOLD = 0.7
INTENT_SCHEMA = {"type": "json_object"}


class IntentClassifier:
    def __init__(self):
        self._llm = Qwen3()

    def classify(self, question: str):
        prompt = f"""
You are an intent classifier for an insurance chatbot.

Choose exactly ONE intent from this list:
- CLAIM_STATUS
- POLICY_STATUS
- ACTIVE_POLICIES_COUNT
- PENDING_CLAIMS

Return JSON ONLY.

OUTPUT FORMAT:
{{
  "intent": "<INTENT_NAME>",
  "confidence": <number between 0 and 1>
}}

QUESTION:
"{question}"
"""
        raw = self._llm.invoke_llm(
            prompt,
            response_format=INTENT_SCHEMA,
        )

        try:
            data = json.loads(raw["content"])
            intent = data.get("intent")
            confidence = float(data.get("confidence", 0.0))

            if intent not in ALLOWED_INTENTS:
                return IntentResult(Intent.UNKNOWN, 0.0)

            if confidence < CONFIDENCE_THRESHOLD:
                return IntentResult(Intent.UNKNOWN, confidence)

            return IntentResult(Intent(intent), float(confidence))
        except Exception:
            return IntentResult(Intent.UNKNOWN, 0.0)
