import os
import pickle
import gdown  # Install using: pip install gdown

# Google Drive shared file links
model_url = "https://drive.google.com/file/d/1wh_tMKLQGBWFPQSMdSfmfwJ4vCcxsjLR/view?usp=drive_link"
vectorizer_url = "https://drive.google.com/file/d/1LDj3a8fJaN00vWtD2fIbkZ1CAd6NZHNQ/view?usp=drive_link"

# Download files locally
if not os.path.exists('./src/model.pkl'):
    gdown.download(model_url, './src/model.pkl', quiet=False)
if not os.path.exists('./src/vectorizer.pkl'):
    gdown.download(vectorizer_url, './src/vectorizer.pkl', quiet=False)

# Load model and vectorizer
with open('./src/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('./src/vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Function to predict sentiment
def predict_sentiment(text):
    text_tfidf = vectorizer.transform([text])
    sentiment = model.predict(text_tfidf)[0]
    return sentiment

# Test the function
text = "The food was great and the service was excellent!"
sentiment = predict_sentiment(text)
print(f"Predicted sentiment: {sentiment}")
