from src.rag.intent import classify_intent

test_questions = [
    "What is the status of my claim?",
    # "Show policy status for policy P123",
    # "How many active policies do I have?",
    # "List pending claims",
    # "Give me all customer data",
]


def test_intents():
    for q in test_questions:
        result = classify_intent(q)
        print("-" * 50)
        print(f"Question   : {q}")
        print(f"Intent     : {result.intent}")
        print(f"Confidence : {result.confidence}")
