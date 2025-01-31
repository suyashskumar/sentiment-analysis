import os
import sys
import json
import joblib  # Use joblib instead of pickle
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables from .env
load_dotenv()

api_key = os.getenv('API_KEY')
model_file_id = os.getenv('MODEL_FILE_ID')  # File ID from Google Drive
vectorizer_file_id = os.getenv('VECTORIZER_FILE_ID')  # File ID from Google Drive
genai.configure(api_key=api_key)

# Configure generative AI model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 350,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat()

# Authenticate with Google Drive API
def authenticate_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive.readonly'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive.readonly'])
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

# Download file from Google Drive
def download_file(file_id, destination):
    try:
        drive_service = authenticate_drive()
        request = drive_service.files().get_media(fileId=file_id)
        with open(destination, 'wb') as file:
            request.execute()
    except Exception as e:
        print(f"Error downloading file: {e}", file=sys.stderr)

# Function to load model and vectorizer
def load_model_and_vectorizer():
    model_path = "sentiment_model.sav"
    vectorizer_path = "vectorizer.sav"

    # Download model and vectorizer from Google Drive
    download_file(model_file_id, model_path)
    download_file(vectorizer_file_id, vectorizer_path)

    # Load using joblib
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return model, vectorizer

# Function to predict sentiment
def predict_sentiment(text):
    try:
        model, vectorizer = load_model_and_vectorizer()
        text_tfidf = vectorizer.transform([text])
        sentiment = model.predict(text_tfidf)[0]
        return sentiment
    except Exception as e:
        print(f"Error in predict_sentiment: {e}", file=sys.stderr)
        return None

# Function to map sentiment score to star rating
def sentiment_to_stars(sentiment):
    sentiment_map = {
        0: "Extremely Negative (1 Star)",
        1: "Slightly Negative (2 Star)",
        2: "Neutral (3 Star)",
        3: "Slightly Positive (4 Star)",
        4: "Extremely Positive (5 Star)"
    }
    return sentiment_map.get(sentiment, "Unknown Sentiment")

# Function to generate feedback using AI
def generate_feedback(text, sentiment):
    try:
        sentiment_label = sentiment_to_stars(sentiment)
        feedback_prompt = f"Analyze why {text} is considered {sentiment_label}. Provide feedback within 150-200 words."
        response = model.generate_content(feedback_prompt)
        feedback = response.text
        return feedback
    except Exception as e:
        print(f"Error in generate_feedback: {e}", file=sys.stderr)
        return "Unable to generate feedback."

if __name__ == '__main__':
    text = sys.argv[1]  # Get input from command line
    
    # Predict sentiment
    sentiment = predict_sentiment(text)
    sentiment_label = sentiment_to_stars(sentiment)
    
    # Generate feedback
    feedback = generate_feedback(text, sentiment)
    
    # Return sentiment label and feedback as JSON
    result = {
        'sentiment_label': sentiment_label,
        'feedback': feedback
    }
    
    print(json.dumps(result))