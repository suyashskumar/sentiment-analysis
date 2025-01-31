// Auto-resize textarea based on input
function resizeTextarea() {
    const textarea = document.getElementById('inputText');
    textarea.style.height = 'auto';  // Reset height to recalculate it
    textarea.style.height = `${textarea.scrollHeight}px`;  // Adjust height dynamically
}

// Function to handle sentiment analysis request
async function getSentiment() {
    const text = document.getElementById('inputText').value.trim();
    const resultElement = document.getElementById('result');

    // Check for empty input
    if (!text) {
        alert('Please enter some text.');
        return;
    }

    // Show loading state
    resultElement.innerText = 'Analyzing sentiment...';
    resultElement.className = 'loading'; 

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) throw new Error('Server error, please try again.');

        const { sentiment, feedback } = await response.json();
        console.log('Sentiment:', sentiment);
        console.log('Feedback:', feedback);

        // Display the result
        resultElement.innerHTML = `<strong>Predicted Sentiment:</strong> ${sentiment} <br><br>
                                   <strong>Analysis & Feedback:</strong> <br>${feedback}`;

        // Update sentiment-based styling
        updateSentimentClass(resultElement, sentiment);

    } catch (error) {
        console.error('Error:', error);
        resultElement.innerText = 'Error occurred, please try again.';
        resultElement.className = 'error';
    }
}

// Function to dynamically update sentiment styling
function updateSentimentClass(element, sentiment) {
    element.classList.remove('extremely-positive', 'slightly-positive', 'neutral', 'slightly-negative', 'extremely-negative', 'other');

    if (sentiment.includes('Extremely Positive')) {
        element.classList.add('extremely-positive');
    } else if (sentiment.includes('Slightly Positive')) {
        element.classList.add('slightly-positive');
    } else if (sentiment.includes('Neutral')) {
        element.classList.add('neutral');
    } else if (sentiment.includes('Slightly Negative')) {
        element.classList.add('slightly-negative');
    } else if (sentiment.includes('Extremely Negative')) {
        element.classList.add('extremely-negative');
    } else {
        element.classList.add('other');
    }
}

// Function to toggle sidebar visibility
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
}
