// Function to handle the form submission and get the prediction
async function getSentiment() {
    const text = document.getElementById('inputText').value;

    // Check if the input is not empty
    if (text.trim() === '') {
        alert('Please enter some text.');
        return;
    }

    // Display loading message and reset previous state
    const resultElement = document.getElementById('result');
    resultElement.innerText = 'Analyzing sentiment...';
    resultElement.className = 'loading'; // Add a class for styling the loading state

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }), // Send input text to the server
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.error) {
            // Handle Python-side errors
            throw new Error(result.error);
        }

        // Get sentiment from the result and map it to stars
        const sentiment = result.sentiment; // Assumes the server returns sentiment as 0–4
        const sentimentLabel = sentimentToStars(sentiment);

        // Display sentiment result
        resultElement.innerText = `Predicted Sentiment: ${sentimentLabel}`;
        resultElement.className = ''; // Reset classes
        resultElement.classList.add(`sentiment-${sentiment}`); // Apply sentiment-specific class
    } catch (error) {
        console.error('Error:', error);

        // Display error message to the user
        resultElement.innerText = 'Error occurred, please try again.';
        resultElement.className = 'error'; // Add a class for styling error messages
    }
}

// Map sentiment score (0 to 4) to textual descriptions
function sentimentToStars(sentiment) {
    const sentimentMap = {
        0: "Extremely Negative (1 Star)",
        1: "Slightly Negative (2 Stars)",
        2: "Neutral (3 Stars)",
        3: "Slightly Positive (4 Stars)",
        4: "Extremely Positive (5 Stars)",
    };
    return sentimentMap[sentiment] || "Unknown Sentiment";
}

// Function to toggle the sidebar visibility
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active'); // Toggle the 'active' class to show/hide sidebar
}
// Function to handle the form submission and get the prediction
async function getSentiment() {
    const text = document.getElementById('inputText').value;

    // Check if the input is not empty
    if (text.trim() === '') {
        alert('Please enter some text.');
        return;
    }

    // Display loading message and reset previous state
    const resultElement = document.getElementById('result');
    resultElement.innerText = 'Analyzing sentiment...';
    resultElement.className = 'loading'; // Add a class for styling the loading state

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }), // Send input text to the server
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.error) {
            // Handle Python-side errors
            throw new Error(result.error);
        }

        // Get sentiment from the result and map it to stars
        const sentiment = result.sentiment; // Assumes the server returns sentiment as 0–4
        const sentimentLabel = sentimentToStars(sentiment);

        // Display sentiment result
        resultElement.innerText = `Predicted Sentiment: ${sentimentLabel}`;
        resultElement.className = ''; // Reset classes
        resultElement.classList.add(`sentiment-${sentiment}`); // Apply sentiment-specific class
    } catch (error) {
        console.error('Error:', error);

        // Display error message to the user
        resultElement.innerText = 'Error occurred, please try again.';
        resultElement.className = 'error'; // Add a class for styling error messages
    }
}

// Map sentiment score (0 to 4) to textual descriptions
function sentimentToStars(sentiment) {
    const sentimentMap = {
        0: "Extremely Negative (1 Star)",
        1: "Slightly Negative (2 Stars)",
        2: "Neutral (3 Stars)",
        3: "Slightly Positive (4 Stars)",
        4: "Extremely Positive (5 Stars)",
    };
    return sentimentMap[sentiment] || "Unknown Sentiment";
}

// Function to toggle the sidebar visibility
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active'); // Toggle the 'active' class to show/hide sidebar
}
// Function to handle the form submission and get the prediction
async function getSentiment() {
    const text = document.getElementById('inputText').value;

    // Check if the input is not empty
    if (text.trim() === '') {
        alert('Please enter some text.');
        return;
    }

    // Display loading message and reset previous state
    const resultElement = document.getElementById('result');
    resultElement.innerText = 'Analyzing sentiment...';
    resultElement.className = 'loading'; // Add a class for styling the loading state

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }), // Send input text to the server
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.error) {
            // Handle Python-side errors
            throw new Error(result.error);
        }

        // Get sentiment from the result and map it to stars
        const sentiment = result.sentiment; // Assumes the server returns sentiment as 0–4
        const sentimentLabel = sentimentToStars(sentiment);

        // Display sentiment result
        resultElement.innerText = `Predicted Sentiment: ${sentimentLabel}`;
        resultElement.className = ''; // Reset classes
        resultElement.classList.add(`sentiment-${sentiment}`); // Apply sentiment-specific class
    } catch (error) {
        console.error('Error:', error);

        // Display error message to the user
        resultElement.innerText = 'Error occurred, please try again.';
        resultElement.className = 'error'; // Add a class for styling error messages
    }
}

// Map sentiment score (0 to 4) to textual descriptions
function sentimentToStars(sentiment) {
    const sentimentMap = {
        0: "Extremely Negative (1 Star)",
        1: "Slightly Negative (2 Stars)",
        2: "Neutral (3 Stars)",
        3: "Slightly Positive (4 Stars)",
        4: "Extremely Positive (5 Stars)",
    };
    return sentimentMap[sentiment] || "Unknown Sentiment";
}

// Function to toggle the sidebar visibility
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active'); // Toggle the 'active' class to show/hide sidebar
}
