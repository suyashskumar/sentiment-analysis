import sys
import json
import os
import pickle
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import google.generativeai as genai
from dotenv import load_dotenv
from webscraper import scrape_comments
 
sys.path.append(os.path.abspath('./src'))  # Add the src directory to sys.path
 
load_dotenv()
 
parent_directory = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(parent_directory, "sentiment_comments.csv")
if not os.path.exists(csv_path):
    print(f"Error: CSV file not found at {csv_path}", file=sys.stderr)
    sys.exit(1)
 
dataset = pd.read_csv(csv_path)
dataset.columns = dataset.columns.str.lower()
# Prepare the data
X = dataset['comment']
y = dataset['sentiment']
 
# Define the train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
# Train the model
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
 
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)
 
model_path = os.path.join(parent_directory, "model.pkl")
vectorizer_path = os.path.join(parent_directory, "vectorizer.pkl")

with open(model_path, 'wb') as model_file:
    pickle.dump(model, model_file)
with open(vectorizer_path, 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)
 
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

# Create the generative AI model
generation_config = {
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 30,
  "max_output_tokens": 150,
  "response_mime_type": "text/plain",
}

gen_model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = gen_model.start_chat()
 
# Load model and vectorizer once
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)
with open(vectorizer_path, 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric shapes
        "\U0001F800-\U0001F8FF"  # Supplemental symbols
        "\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
        "\U0001FA00-\U0001FA6F"  # Chess symbols, medical symbols, etc.
        "\U0001FA70-\U0001FAFF"  # More supplemental symbols
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)
 
# Predict sentiment function
def predict_sentiment(text):
    try:
        text=remove_emojis(text)
        text_tfidf = vectorizer.transform([text])
        sentiment = model.predict(text_tfidf)[0]
        return sentiment
    except Exception as e:
        print(f"Error in predict_sentiment: {e}", file=sys.stderr)
        return None
 
# Function to map sentiment to stars
def sentiment_to_stars(sentiment):
    sentiment_map = {
        0: "Extremely Negative (1 Star)",
        1: "Slightly Negative (2 Stars)",
        2: "Neutral (3 Stars)",
        3: "Slightly Positive (4 Stars)",
        4: "Extremely Positive (5 Stars)"
    }
    return sentiment_map.get(sentiment, "Unknown Sentiment")
 
# Function to generate feedback
def generate_feedback(text, sentiment):
    try:
        text=remove_emojis(text)
        sentiment_label = sentiment_to_stars(sentiment)
        feedback_prompt = f"Analyze why {text} is considered {sentiment_label} by the customer who provided the input. Provide feedback in paragraph format without headers. Limit it to 100 words max."
        response = gen_model.generate_content(feedback_prompt)
        return response.text
    except Exception as e:
        print(f"Error in generate_feedback: {e}", file=sys.stderr)
        return "Unable to generate feedback."
 
# Analyze sentiment for multiple comments (from URL)

def analyze_sentiment(url=None):
    try:
        # Ensure `url` is a dictionary if passed as a JSON string
        if isinstance(url, str):
            try:
                url = json.loads(url)  # Convert JSON string to dictionary
            except json.JSONDecodeError:
                return json.dumps({"error": "Invalid JSON input"})

        if not isinstance(url, dict) or "url" not in url:
            return json.dumps({"error": "Missing or invalid 'url' parameter."})

        url = url["url"]  # Extract the actual URL

        comment_response = scrape_comments(url)

        if not isinstance(comment_response, dict):  # Ensure we get a dictionary
            return json.dumps({"error": "Invalid response from scrape_comments"})

        comments = comment_response.get("comments", [])

        if not comments:
            return json.dumps({"error": "No comments found or failed to scrape comments."})

        sentiment_data = []
        graph_data = []

        for comment in comments:
            sentiment = predict_sentiment(comment)
            sentiment_label = sentiment_to_stars(sentiment)
            sentiment_data.append({"comment": comment, "sentiment": sentiment_label})
            graph_data.append(sentiment)

        print(f"Graph Data: {graph_data}", file=sys.stderr)

        analysis_prompt = f"Here is a series of sentiment values (scale 0-4) based on customer reviews: {graph_data}. Provide an analysis of this trend in simple terms."
        analysis_response = gen_model.generate_content(analysis_prompt)

        print(f"Analysis Response: {analysis_response}", file=sys.stderr)

        if not isinstance(analysis_response, dict):
            return json.dumps({"error": "Invalid response from analysis model."})

        analysis_text = analysis_response.get('text', 'No analysis available.')

        result = {
            "sentiment_data": sentiment_data,
            "graph_data": graph_data,
            "analysis_summary": analysis_text
        }
        return json.dumps(result)

    except Exception as e:
        print(f"Error in analyze_sentiment: {e}", file=sys.stderr)
        return json.dumps({"error": "Analysis failed."})
 
# CLI execution
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        print(analyze_sentiment())
    elif len(sys.argv) > 1 and sys.argv[1] == "url" and len(sys.argv) > 2:
        url = sys.argv[2]
        print(analyze_sentiment(url))
    else:
        text = sys.argv[1]
        sentiment = predict_sentiment(text)
        sentiment_label = sentiment_to_stars(sentiment)
        feedback = generate_feedback(text, sentiment)
 
        result = {
            'sentiment_label': sentiment_label,
            'feedback': feedback
        }
 
        print(json.dumps(result))