import sys
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import google.generativeai as genai

from sentiment_model import predict_sentiment

sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Configure Gemini AI
genai.configure(api_key=api_key)

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

# Define file paths
parent_directory = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(parent_directory, 'reddit_comments.csv')
model_path = os.path.join(parent_directory, 'model.pkl')
vectorizer_path = os.path.join(parent_directory, 'vectorizer.pkl')
public_folder = os.path.join(parent_directory, '../public')
graph_path = os.path.join(public_folder, 'sentiment_distribution.png')  
analysis_path = os.path.join(public_folder, 'analysis.txt')  

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

def generate_sentiment_distribution(sentiment_data):
    sentiment_counts = sentiment_data.value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    plt.plot(sentiment_counts.index, sentiment_counts.values, marker='o', linestyle='-', color='b')

    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment Labels")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.savefig(graph_path)
    plt.close()
    print(f"Sentiment graph saved as {graph_path}")

    # Pass sentiment_counts to analysis function
    analyze_graph_with_ai(sentiment_counts)


# Analyze sentiment trends instead of using raw image bytes
def analyze_graph_with_ai(sentiment_counts):
    try:
        # Convert sentiment data into a readable format
        sentiment_summary = "\n".join([f"Sentiment {label}: {count}" for label, count in sentiment_counts.items()])

        # Create a meaningful prompt
        prompt = (
            f"Analyze the following sentiment distribution and provide insights:\n\n"
            f"{sentiment_summary}\n\n"
            f"Describe any trends, unusual patterns, or key observations."
        )

        # Send the text-based prompt to Gemini AI
        response = gen_model.generate_content(prompt)
        
        # Save analysis to file
        with open(analysis_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        print("\nAI Analysis saved to analysis.txt")
    
    except Exception as e:
        print(f"Error analyzing sentiment data with AI: {e}", file=sys.stderr)

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