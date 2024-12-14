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
        const result = await response.json();
        // Display the sentiment result
        const sentiment = result.sentiment;
        resultElement.innerText = `Predicted Sentiment: ${sentiment}`;
        // Change the result color based on sentiment
        if (sentiment === 'positive') {
            resultElement.style.color = '#28a745'; // Green for positive sentiment
        } else if (sentiment === 'negative') {
            resultElement.style.color = '#dc3545'; // Red for negative sentiment
        } else {
            resultElement.style.color = '#ffc107'; // Yellow for neutral sentiment
        }
    } catch (error) {
        console.error('Error:', error);
        resultElement.innerText = 'Error occurred, please try again.';
        resultElement.style.color = '#dc3545'; // Red for error message
    }
}

// Function to toggle the sidebar visibility
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}