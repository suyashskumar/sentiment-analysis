import sys
import json
import os
import pickle
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB  # Change here for Naive Bayes
from sklearn.model_selection import train_test_split
import google.generativeai as genai
from dotenv import load_dotenv
sys.path.append(os.path.abspath('./src'))  # Add the src directory to the sys.path

load_dotenv()

# Load dataset from Hugging Face
ds = load_dataset("Yelp/yelp_review_full")

# Limit the dataset size by selecting only the first 20,000 samples
dataset = ds['train'].select(range(20000))

# Convert to DataFrame for easier handling
dataset = dataset.to_pandas()

# Prepare the data
X = dataset['text']
y = dataset['label']

# Define the train-test ratio
train_size = 0.8
test_size = 0.2

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

# Train the model
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

model = MultinomialNB()  # Naive Bayes
model.fit(X_train_tfidf, y_train)

# Save the model and vectorizer
with open('./src/model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
with open('./src/vectorizer.pkl', 'wb') as vec_file:
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
with open('./src/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('./src/vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Predict sentiment function
def predict_sentiment(text):
    try:
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
        1: "Slightly Negative (2 Star)",
        2: "Neutral (3 Star)",
        3: "Slightly Positive (4 Star)",
        4: "Extremely Positive (5 Star)"
    }
    return sentiment_map.get(sentiment, "Unknown Sentiment")

# Function to generate feedback
def generate_feedback(text, sentiment):
    try:
        sentiment_label = sentiment_to_stars(sentiment)
        feedback_prompt = f"Analyze why {text} is considered {sentiment_label} by the customer who provided the input. Provide feedback in paragraph format without headers for the same."
        response = gen_model.generate_content(feedback_prompt)
        return response.text
    except Exception as e:
        print(f"Error in generate_feedback: {e}", file=sys.stderr)
        return "Unable to generate feedback."

### **NEW FUNCTION: analyzeSentiment() for multiple comments** ###
def analyzeSentiment():
    try:
        from webscraper import scrape_comments
        # Scrape comments using webscraper.py
        comments = scrape_comments()  # Ensure webscraper.py returns a list of comments

        if not comments:
            return json.dumps({"error": "No comments found."})

        sentiment_data = []
        graph_data = []

        for comment in comments:
            sentiment = predict_sentiment(comment)
            sentiment_label = sentiment_to_stars(sentiment)
            sentiment_data.append({"comment": comment, "sentiment": sentiment_label})

            # Append numerical sentiment value for graph
            graph_data.append(sentiment)

        # Use generative AI to analyze trends
        analysis_prompt = f"Here is a series of sentiment values (scale 0-4) based on customer reviews: {graph_data}. Provide an analysis of this trend in simple terms."
        analysis_response = gen_model.generate_content(analysis_prompt)
        analysis_text = analysis_response.text

        # Return JSON response with sentiment data and graph analysis
        result = {
            "sentiment_data": sentiment_data,
            "graph_data": graph_data,
            "analysis_summary": analysis_text
        }
        return json.dumps(result)

    except Exception as e:
        print(f"Error in analyzeSentiment: {e}", file=sys.stderr)
        return json.dumps({"error": "Analysis failed."})

# CLI execution
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        print(analyzeSentiment())
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