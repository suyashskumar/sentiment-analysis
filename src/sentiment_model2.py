import pandas as pd
import pickle
import os
import sys
import mysql.connector
import matplotlib.pyplot as plt
from sentiment_model import predict_sentiment

# Define paths for the dataset and model files
csv_path = "./reddit_comments.csv"
model_path = "./model.pkl"
vectorizer_path = "./vectorizer.pkl"

# Function to confirm the existence of files
def check_files():
    if not os.path.exists(csv_path):
        print(f" ERROR: CSV file not found at {csv_path}")
        return False
    if not os.path.exists(model_path):
        print(" ERROR: Model file not found!")
        return False
    if not os.path.exists(vectorizer_path):
        print(" ERROR: Vectorizer file not found!")
        return False
    print(f"All necessary files are found. Proceeding...")
    return True
# Specify the path for the CSV file
parent_directory = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(parent_directory, 'reddit_comments.csv')
if not os.path.exists(csv_path):
    print(f"Error: 'reddit_comments.csv' not found in the parent directory.", file=sys.stderr)
    sys.exit(1)

print(f"Using the CSV file: reddit_comments.csv")
dataset = pd.read_csv(csv_path)
dataset.columns = dataset.columns.str.lower()

# Database connection setup
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='ANU123@anu',  # Replace with your MySQL password
            database='sentiment_analysis'  # Replace with your database name
        )
        print("Connected to the database successfully.")  # Check if connection is successful
        return connection
    except Exception as e:
        print(f"Error in database connection: {e}", file=sys.stderr)
        return None

# Function to store sentiment score in the database
def store_sentiment_in_db(comment, sentiment_score, file_name):
    try:
        # Connect to the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Prepare SQL query for inserting sentiment data into 'bulk_sentiment_results'
        insert_query = """
            INSERT INTO bulk_sentiment_results (file_name, comment, sentiment_score)
            VALUES (%s, %s, %s)
        """
        
        # Insert the comment and its sentiment score into the database
        cursor.execute(insert_query, (file_name, comment, sentiment_score))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error in store_sentiment_in_db: {e}", file=sys.stderr)

# Function to generate sentiment distribution graph
def generate_sentiment_distribution(sentiment_data):
    sentiment_counts = sentiment_data.value_counts()
    sentiment_counts.plot(kind='bar', title="Sentiment Distribution")
    plt.xlabel('Sentiment Labels')
    plt.ylabel('Frequency')
    plt.show()

# Function for bulk sentiment analysis
def bulk_sentiment_analysis(dataset):
    if not check_files():
        return

    # Load model and vectorizer
    print("Loading model and vectorizer...")
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(vectorizer_path, 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)

    # Load dataset
    dataset = pd.read_csv(csv_path)
    dataset.columns = dataset.columns.str.strip()
    print("Dataset columns:", dataset.columns)

    print(f"Loaded dataset from {csv_path}")
    
    # Extract comments from dataset
    comments = dataset['Comment'].tolist()
    print(f"Extracted {len(comments)} comments from the dataset.")

    # List to hold sentiment labels
    sentiment_labels = []
    
    # Process each comment
    for idx, Comment in enumerate(comments):
        print(f"Analyzing comment {idx+1}/{len(comments)}: {Comment[:50]}...")

        # Predict sentiment
        sentiment = predict_sentiment(Comment, model, vectorizer) # Pass model and vectorizer
        print(f"Sentiment prediction (0-4) for comment {idx+1}: {sentiment}")
        sentiment_labels.append(sentiment)

        # Store in the database
        store_sentiment_in_db(Comment, sentiment, "reddit_comments.csv")  # Pass file name as 'reddit_comments.csv'

        print(f"Sentiment prediction (0-4) for comment {idx+1}: {sentiment}")

    # Store sentiment labels in a DataFrame for visualization
    sentiment_data = pd.Series(sentiment_labels)

    # Generate sentiment distribution graph
    generate_sentiment_distribution(sentiment_data)

    print("Bulk sentiment analysis completed.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        # Perform bulk sentiment analysis
        result = bulk_sentiment_analysis(dataset)
        print(result)
    else:
        print("Usage: python sentiment_model2.py batch")
