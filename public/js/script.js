function resizeTextarea() {
    var textarea = document.getElementById('inputText');
    textarea.style.height = 'auto';  // Reset height to auto to recalculate it
    textarea.style.height = (textarea.scrollHeight) + 'px';  // Set height based on scrollHeight
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
        const result = await response.json();
        const { sentiment, feedback } = result;

        console.log('Sentiment:', sentiment); // Log the sentiment value (0-4)
        console.log('Feedback:', feedback);

        // Display the sentiment result
        resultElement.innerText = `Predicted Sentiment: ${sentiment}\n\nAnalysis & Feedback:\n\n${feedback}`;
        
        // Dynamically add a class based on the sentiment
        resultElement.classList.remove('extremely-positive', 'slightly-positive', 'neutral', 'slightly-negative', 'extremely-negative', 'other');
        
        if (sentiment.includes('Extremely Positive')) {
            resultElement.classList.add('extremely-positive');
        } else if (sentiment.includes('Slightly Positive')) {
            resultElement.classList.add('slightly-positive');
        } else if (sentiment.includes('Neutral')) {
            resultElement.classList.add('neutral');
        } else if (sentiment.includes('Slightly Negative')) {
            resultElement.classList.add('slightly-negative');
        } else if (sentiment.includes('Extremely Negative')) {
            resultElement.classList.add('extremely-negative');
        } else {
            resultElement.classList.add('other');
        }
    } catch (error) {
        console.error('Error:', error);
        resultElement.innerText = 'Error occurred, please try again.';
        resultElement.classList.add('error');
    }
}

// Function to toggle the sidebar visibility
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}