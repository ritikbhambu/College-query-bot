import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

 
df = pd.read_csv("intents.csv")

model = Pipeline([
    ('tfidf', TfidfVectorizer()),         
    ('clf', MultinomialNB())              
])

model.fit(df['Text'], df['Intent'])

joblib.dump(model, 'intent_classifier.pkl')
print("Model trained and saved as 'intent_classifier.pkl'")
