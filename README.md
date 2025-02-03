# Sentiment Analysis for Brand Monitoring

This project is a sentiment analysis application that predicts sentiment from text input and provides feedback using a generative AI model. It includes a web-based frontend for user interaction and a backend powered by Python, Node.js, and MySQL for data storage.

## Features

1. **Sentiment Analysis**: Classifies sentiment as Extremely Negative, Slightly Negative, Neutral, Slightly Positive, or Extremely Positive.
2. **Feedback Generation**: Provides detailed AI-generated feedback explaining the sentiment.
3. **Brand Monitoring**: Scrapes and analyzes sentiment from brand-related web pages.
4. **Database Storage**: Stores user inputs, sentiment analysis results, and monitored brand data.
5. **Interactive User Interface**: Real-time feedback display and dynamic UI elements.
6. **History Tracking**: Allows users to view past sentiment analyses.

## Technologies Used

- **Backend**:
  - Python for sentiment analysis and AI integration.
  - Node.js and Express.js for handling API requests.
  - MySQL for database storage.
- **Frontend**:
  - HTML, CSS, and JavaScript for UI.
  - EJS templates for dynamic content rendering.
- **Dependencies**:
  - `scikit-learn` for text vectorization and classification.
  - `google-generativeai` for AI-driven feedback.
  - `praw` for Reddit scraping.
  - `dotenv` for environment variable management.

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js and npm
- MySQL database
- Git
- Virtual environment (optional but recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sentiment-analysis.git
   cd sentiment-analysis
   ```

2. Install Python dependencies:
   ```bash
   python -m venv venv  # Optional: Create a virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   npm install
   ```

4. Set up the MySQL database:
   - Create a MySQL database and user.
   - Execute `sentiment_analysis.sql` in your MySQL instance:
     ```bash
     mysql -u your_user -p your_database < sentiment_analysis.sql
     ```
   - Configure database credentials in `.env`:
     ```plaintext
     DB_HOST=your_db_host
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_NAME=sentiment_analysis
     API_KEY=your_google_genai_api_key
     ```

5. Run the Node.js server:
   ```bash
   npm start
   ```
   or
   ```bash
   node app.js
   ```

6. Access the application at `http://localhost:3000`.

## Database Schema

- **`sentiment_inputs`**: Stores user-inputted text and sentiment results.
  - `id` (INT, Primary Key, Auto Increment)
  - `input_text` (TEXT, User input)
  - `sentiment_label` (VARCHAR, Sentiment classification)
  - `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

- **`brand_monitoring`**: Stores monitored brands and scraped webpage links.
  - `id` (INT, Primary Key, Auto Increment)
  - `brand_name` (VARCHAR, Unique, Brand name)
  - `scraped_page_link` (VARCHAR, Scraped URL)
  - `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

## File Structure

```
sentiment-analysis/
├── public/                   # Static assets (CSS, JavaScript, images)
├── src/                      # Python scripts
│   ├── sentiment_model.py    # Sentiment prediction and feedback generation
│   ├── webscraper.py         # Scrapes data from Reddit and webpages
│   ├── csv_generator.py      # Handles CSV export of sentiment data
├── views/                    # EJS templates for frontend rendering
│   ├── index.ejs             # Home page
│   ├── history.ejs           # Past sentiment results
│   ├── custom_input.ejs      # Manual sentiment input
│   ├── brands.ejs            # Brand sentiment analysis
├── database/                 # Database scripts
│   ├── sentiment_analysis.sql # Database schema
├── .env                      # Environment variables
├── app.js                    # Node.js backend
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies
└── README.md                 # Project documentation
```

## Usage

1. Open the web application in your browser.
2. Enter text manually or analyze a brand’s sentiment from a scraped webpage.
3. View sentiment classification and AI-generated feedback.
4. Monitor brand sentiment over time using the history page.

## Key Functions

### Python Backend
- **`analyze_sentiment(text)`**: Uses Naive Bayes to classify sentiment.
- **`generate_feedback(text, sentiment)`**: AI-generated explanation for the sentiment.
- **`scrape_reddit(subreddit, limit)`**: Extracts posts for sentiment analysis.

### Frontend JavaScript
- **`resizeTextarea()`**: Dynamically adjusts the textarea height.
- **`analyzeSentiment()`**: Calls the `/analyze` endpoint to process text.
- **`toggleSidebar()`**: Toggles the sidebar navigation.

### Node.js Server
- **`/`**: Serves the home page.
- **`/analyze`**: Triggers sentiment analysis and returns results.
- **`/history`**: Retrieves past sentiment analysis records.
- **`/brands`**: Allows brand monitoring and sentiment tracking.

## Acknowledgements

- **Hugging Face** for datasets.
- **Google Generative AI** for sentiment feedback.
- **PRAW** for Reddit data extraction.