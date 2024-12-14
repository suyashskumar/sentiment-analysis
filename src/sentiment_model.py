import sys
import pickle
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from transformers import pipeline  # Import Hugging Face pipeline for text generation

# Load dataset from Hugging Face
ds = load_dataset("Yelp/yelp_review_full")

# Limit the dataset size by selecting only the first 20,000 samples
dataset = ds['train'].select(range(20000))  # Select first 20,000 rows

# Convert to DataFrame for easier handling
dataset = dataset.to_pandas()

# Prepare the data
X = dataset['text']
y = dataset['label']

# Define the train-test ratio
train_size = 0.8  # 80% for training
test_size = 0.2   # 20% for testing

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

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

# Initialize Hugging Face's text generation pipeline (you can change the model if needed)
generator = pipeline("text-generation", model="gpt2", pad_token_id=50256)

# Function to predict sentiment
def predict_sentiment(text):
    try:
        with open('./src/model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('./src/vectorizer.pkl', 'rb') as vec_file:
            vectorizer = pickle.load(vec_file)

        text_tfidf = vectorizer.transform([text])
        sentiment = model.predict(text_tfidf)[0]
        return sentiment
    except Exception as e:
        print(f"Error in predict_sentiment: {e}", file=sys.stderr)
        return None

# Function to map sentiment to stars
def sentiment_to_stars(sentiment):
    # Map sentiment values (0-4) to 1-5 star scale
    sentiment_map = {
        0: "Extremely Negative (1 Star)",
        1: "Slightly Negative (2 Star)",
        2: "Neutral (3 Star)",
        3: "Slightly Positive (4 Star)",
        4: "Extremely Positive (5 Star)"
    }
    return sentiment_map.get(sentiment, "Unknown Sentiment")

# Function to generate feedback from a generative model
def generate_feedback(text, sentiment):
    try:
        sentiment_label = sentiment_to_stars(sentiment)
        feedback_prompt = f"Provide why {text} is considered {sentiment_label}."
        feedback = generator(feedback_prompt, max_new_tokens=200)[0]['generated_text']
        return feedback
    except Exception as e:
        print(f"Error in generate_feedback: {e}", file=sys.stderr)
        return "Unable to generate feedback."

if __name__ == '__main__':
    # Example text to analyze
    text = sys.argv[1]
    
    # Predict sentiment
    sentiment = predict_sentiment(text)
    sentiment_label = sentiment_to_stars(sentiment)
    print(sentiment_label)
    
    # Generate feedback
    feedback = generate_feedback(text, sentiment)
    print(feedback)