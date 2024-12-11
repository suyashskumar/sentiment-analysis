import sys
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from datasets import load_dataset

# Load dataset
train_ds = load_dataset("Yelp/yelp_review_full", split="train")
test_ds = load_dataset("Yelp/yelp_review_full", split="test")

# Prepare the data
train_data = {'text': train_ds['text'], 'sentiment': train_ds['label']}
test_data = {'text': test_ds['text'], 'sentiment': test_ds['label']}

train_df = pd.DataFrame(train_data)
test_df = pd.DataFrame(test_data)

X_train = train_df['text']
y_train = train_df['sentiment']

# Train the model
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Save the model and vectorizer
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

# Function to predict sentiment
def predict_sentiment(text):
    # Load the trained model and vectorizer
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)

    # Transform the input text and predict sentiment
    text_tfidf = vectorizer.transform([text])
    sentiment = model.predict(text_tfidf)[0]

    return sentiment

if __name__ == '__main__':
    text = sys.argv[1]  # Get text from the command-line arguments
    sentiment = predict_sentiment(text)
    print(sentiment)  # Output the sentiment for the backend to capture