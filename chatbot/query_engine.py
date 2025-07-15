import joblib

# Load trained intent classifier model
model = joblib.load('intent_classifier.pkl')

# Define list of known subjects (for subject extraction)
KNOWN_SUBJECTS = ["dbms", "math", "os", "cse", "ds", "ai", "ml"]

def tokenize(message):
    return message.lower().replace('?', '').replace('.', '').split()

def extract_query_info(message):
    # Intent prediction (from ML model)
    predicted_intent = model.predict([message])[0]  # string like 'get_attendance'

    # Subject extraction 
    tokens = tokenize(message)
    subject = None
    for token in tokens:
        if token in KNOWN_SUBJECTS:
            subject = token.upper()
            break

    return predicted_intent, subject
