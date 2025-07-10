import spacy

# Load the small English model
nlp = spacy.load("en_core_web_sm")

# Process a sample text
doc = nlp("Hello! How can I check my department information?")

# Print token text, part-of-speech, and dependency info
for token in doc:
    print(token.text, token.pos_, token.dep_)
