import sys
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Import the function from the existing sentiment analysis script
from sentiment_model import predict_sentiment  # Ensure sentiment_model.py is in the same directory or in the Python path

sys.stdout.reconfigure(encoding='utf-8')

# Define file paths
parent_directory = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(parent_directory, 'reddit_comments.csv')
model_path = os.path.join(parent_directory, 'model.pkl')
vectorizer_path = os.path.join(parent_directory, 'vectorizer.pkl')

# Ensure necessary files exist
def check_files():
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found at {csv_path}", file=sys.stderr)
        return False
    if not os.path.exists(model_path):
        print("ERROR: Model file not found!", file=sys.stderr)
        return False
    if not os.path.exists(vectorizer_path):
        print("ERROR: Vectorizer file not found!", file=sys.stderr)
        return False
    print("All necessary files found. Proceeding...")
    return True

# Load dataset
if not os.path.exists(csv_path):
    print(f"Error: 'reddit_comments.csv' not found.", file=sys.stderr)
    sys.exit(1)

dataset = pd.read_csv(csv_path)
dataset.columns = dataset.columns.str.lower()

# Generate sentiment distribution graph
def generate_sentiment_distribution(sentiment_data):
    sentiment_counts = sentiment_data.value_counts().sort_index()
    
    plt.figure(figsize=(8, 5))
    plt.plot(sentiment_counts.index, sentiment_counts.values, marker='o', linestyle='-', color='b')
    
    plt.title("Sentiment Distribution (Line Graph)")
    plt.xlabel("Sentiment Labels")
    plt.ylabel("Frequency")
    plt.grid(True)
    
    plt.show()

# Bulk sentiment analysis
def bulk_sentiment_analysis():
    if not check_files():
        return

    print("Processing dataset...")
    comments = dataset['comment'].tolist()
    print(f"Extracted {len(comments)} comments from dataset.")

    sentiment_labels = []
    
    for idx, comment in enumerate(comments):
        print(f"Analyzing comment {idx+1}/{len(comments)}: {comment[:50]}...".encode("utf-8", "ignore").decode("utf-8"))

        # Call the existing predict_sentiment() function from sentiment_model.py
        sentiment = predict_sentiment(comment)
        
        print(f"Predicted Sentiment: {sentiment}")
        sentiment_labels.append(sentiment)
    
    sentiment_data = pd.Series(sentiment_labels)
    generate_sentiment_distribution(sentiment_data)
    print("Bulk sentiment analysis completed.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        bulk_sentiment_analysis()
    else:
        print("Usage: python sentiment_model2.py batch")