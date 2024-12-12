import sys
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data_path = './data/dataset.csv'
dataset = pd.read_csv(data_path)

# Prepare the data
X = dataset['text']
y = dataset['label']

# Split into training and testing sets
train_size = int(0.8 * len(dataset))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Train the model
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Save the model and vectorizer
with open('./src/model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
with open('./src/vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

# Function to predict sentiment
def predict_sentiment(text):
    with open('./src/model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('./src/vectorizer.pkl', 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)

    text_tfidf = vectorizer.transform([text])
    sentiment = model.predict(text_tfidf)[0]
    return sentiment

if __name__ == '__main__':
    text = sys.argv[1]
    sentiment = predict_sentiment(text)
    print(sentiment)
