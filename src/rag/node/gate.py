DISALLOWED_PATTERNS = ["dump", "export", "all data", "entire database", "password", "secret"]


def hard_gate(question: str) -> bool:
    q = question.lower()
    return not any(p in q for p in DISALLOWED_PATTERNS)
