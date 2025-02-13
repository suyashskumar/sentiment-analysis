import sys
import os
import pickle
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Import the function from the existing sentiment analysis script
from sentiment_model import predict_sentiment  # Ensure sentiment_model.py is in the same directory or in the Python path

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Define file paths
parent_directory = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(parent_directory, 'reddit_comments.csv')
model_path = os.path.join(parent_directory, 'src', 'model.pkl')
vectorizer_path = os.path.join(parent_directory, 'src', 'vectorizer.pkl')

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

# Database connection setup
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,  # Replace with your MySQL username
            password=DB_PASSWORD,  # Replace with your MySQL password
            database=DB_NAME  # Replace with your database name
        )
        print("Connected to the database successfully.")
        return connection
    except Exception as e:
        print(f"Error in database connection: {e}", file=sys.stderr)
        return None

# Store sentiment analysis results in the database
def store_sentiment_in_db(comment, sentiment_score, file_name):
    try:
        conn = get_db_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        
        insert_query = """
            INSERT INTO bulk_sentiment_results (file_name, comment, sentiment_score)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (file_name, comment, sentiment_score))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error in store_sentiment_in_db: {e}", file=sys.stderr)

# Generate sentiment distribution graph
def generate_sentiment_distribution(sentiment_data):
    sentiment_counts = sentiment_data.value_counts()
    sentiment_counts.plot(kind='bar', title="Sentiment Distribution")
    plt.xlabel('Sentiment Labels')
    plt.ylabel('Frequency')
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
        print(f"Analyzing comment {idx+1}/{len(comments)}: {comment[:50]}...")

        # Call the existing predict_sentiment() function from sentiment_model.py
        sentiment = predict_sentiment(comment)
        
        print(f"Predicted Sentiment: {sentiment}")
        sentiment_labels.append(sentiment)
        store_sentiment_in_db(comment, sentiment, "reddit_comments.csv")
    
    sentiment_data = pd.Series(sentiment_labels)
    generate_sentiment_distribution(sentiment_data)
    print("Bulk sentiment analysis completed.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        bulk_sentiment_analysis()
    else:
        print("Usage: python bulk_sentiment_analysis.py batch")