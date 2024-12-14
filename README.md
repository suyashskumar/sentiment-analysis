# Sentiment Analysis for Brand Monitoring

This project is a sentiment analysis application that predicts sentiment from text input and provides feedback using a generative AI model. It includes a web-based frontend for user interaction and a backend powered by Python and Node.js.

## Features

1. **Sentiment Analysis**: Classifies the sentiment of text as Extremely Negative, Slightly Negative, Neutral, Slightly Positive, or Extremely Positive.
2. **Feedback Generation**: Provides detailed feedback explaining the sentiment using a generative AI model.
3. **Dynamic User Interface**: Includes real-time feedback display and dynamic styling based on sentiment.
4. **Interactive Sidebar**: Toggleable sidebar for enhanced user navigation.

## Technologies Used

- **Backend**:
  - Python for sentiment analysis and generative AI integration.
  - Node.js and Express.js for serving the web application and handling API requests.
- **Frontend**:
  - HTML, CSS, and JavaScript for the user interface.
  - EJS templates for rendering dynamic content.
- **Dependencies**:
  - `scikit-learn` for text vectorization and logistic regression.
  - `google-generativeai` for AI-driven feedback generation.
  - `datasets` for loading and managing text data.
  - `dotenv` for managing environment variables.

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js and npm
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

4. Create a `.env` file in the root directory:
   ```plaintext
   API_KEY=your_google_genai_api_key
   ```

   Replace `your_google_genai_api_key` with your actual API key.

5. Run the server:
   ```bash
   npm start
   ```
   or
   ```bash
   node app.js
   ```

7. Access the application at `http://localhost:3000`.

## File Structure

```
sentiment-analysis/
├── public/                   # Static assets (CSS, JavaScript, images)
├── src/                      # Python scripts
│   ├── sentiment_model.py    # Python script for sentiment prediction
├── views/                    # EJS templates
│   ├── index.ejs             # Main web page
├── .env                      # Environment variables
├── app.js                    # Node.js server
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies
└── README.md                 # Project documentation
```

## Usage

1. Open the web application in your browser.
2. Enter the text to analyze in the input box.
3. Submit the text to receive sentiment prediction and feedback.
4. The application dynamically updates the interface to reflect the sentiment.

## Key Functions

### Python Backend
- **`predict_sentiment(text)`**: Predicts sentiment based on input text using logistic regression.
- **`generate_feedback(text, sentiment)`**: Generates feedback using a generative AI model.

### Frontend JavaScript
- **`resizeTextarea()`**: Dynamically adjusts the height of the input textarea.
- **`getSentiment()`**: Sends text input to the backend and displays sentiment and feedback.
- **`toggleSidebar()`**: Toggles the visibility of the sidebar.

### Node.js Server
- **`/`**: Serves the index page.
- **`/predict`**: Handles POST requests for sentiment analysis and feedback generation.
