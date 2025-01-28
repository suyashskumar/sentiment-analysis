-- Create the sentiment_analysis database
CREATE DATABASE IF NOT EXISTS sentiment_analysis;

-- Use the sentiment_analysis database
USE sentiment_analysis;

-- Table to store manual inputs and responses
CREATE TABLE IF NOT EXISTS sentiment_inputs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_text TEXT NOT NULL, -- Input text from the user
    sentiment_label VARCHAR(255) NOT NULL, -- Sentiment label generated
    feedback TEXT NOT NULL, -- Feedback generated
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of entry
);

-- Table to store brands monitored and their scraped webpage links
CREATE TABLE IF NOT EXISTS brand_monitoring (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL UNIQUE, -- Name of the brand
    scraped_page_link VARCHAR(255), -- Link to the scraped webpage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of entry
);