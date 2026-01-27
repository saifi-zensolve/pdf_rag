from src.rag.intent import Intent, IntentClassifier

test_questions = [
    "What is the status of my claim?",
    # "Show policy status for policy P123",
    # "How many active policies do I have?",
    # "List pending claims",
    # "Give me all customer data",
]


def test_intents_claim_status():
    q = "What is the status of my claim?"

    result = IntentClassifier().classify(question=q)

    print(f"Question   : {q}")
    print(f"Intent     : {result.intent}")
    print(f"Confidence : {result.confidence}")

    assert result.intent == Intent.CLAIM_STATUS
    assert result.confidence >= 0.7


# def test_intents_unknown():
#     q = "Give me all customer data"

#     result = IntentClassifier().classify(question=q)

#     print(f"Question   : {q}")
#     print(f"Intent     : {result.intent}")
#     print(f"Confidence : {result.confidence}")

#     assert result.intent == Intent.UNKNOWN
#     assert result.confidence == 0.0
