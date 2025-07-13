# chatbot/query_engine.py

def tokenize(message):
    return message.lower().replace('?', '').replace('.', '').split()

def extract_query_info(message):
    tokens = tokenize(message)

    # Possessive check
    if any(word in tokens for word in ["friend", "friends", "his", "her", "their", "someone"]):
        return "unsupported", None

    # Intent detection
    if "attendance" in tokens:
        intent = "attendance"
    elif "marks" in tokens or "score" in tokens:
        intent = "marks"
    elif "faculty" in tokens or "teacher" in tokens:
        intent = "faculty"
    else:
        intent = None

    # Subject detection
    subjects = ["dbms", "math", "os", "cse", "ds", "ai", "ml"]
    subject = None
    for token in tokens:
        if token in subjects:
            subject = token.upper()
            break

    return intent, subject
