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
        if (resultElement) {
            resultElement.innerHTML = `<strong>Predicted Sentiment:</strong> ${sentiment} <br><br>
                                    <strong>Analysis & Feedback:</strong> <br>${feedback}`;
            // Update sentiment-based styling
            updateSentimentClass(resultElement, sentiment);
        }

    } catch (error) {
        console.error('Error:', error);
        if (resultElement) {
            resultElement.innerText = 'Error occurred, please try again.';
            resultElement.className = 'error';
        }
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

// Function to handle bulk sentiment analysis request
async function analyzeSentiment() {
    const url = document.getElementById('urlInput').value.trim();
    const resultElement = document.getElementById('result');
    const feedbackElement = document.getElementById('analysisText');

    if (!url) {
        alert('Please enter a URL.');
        return;
    }

    resultElement.innerText = 'Scraping and analyzing the webpage...';
    resultElement.className = 'loading'; 

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url }),
        });

        if (!response.ok) throw new Error('Server error, please try again.');

        const analysisResults = await response.json();

        // Update the result section with the analysis results
        feedbackElement.innerHTML = `<strong>Analysis & Feedback:</strong> <br>${analysisResults.analysis_summary}`;
        resultElement.innerHTML = `<strong>Sentiment Analysis Completed:</strong> <br><br>`;
    } catch (error) {
        console.error('Error:', error);
        resultElement.innerText = 'Error occurred, please try again.';
        resultElement.className = 'error';
    }
}

// Function to toggle sidebar visibility
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
}

/** ======= Line Graph for Sentiment Trends (ADDED) ======= **/
// Sentiment Mapping (0-4 Scale)
const sentimentMap = {
    "Extremely Negative (1 Star)": 0,
    "Slightly Negative (2 Star)": 1,
    "Neutral (3 Star)": 2,
    "Slightly Positive (4 Star)": 3,
    "Extremely Positive (5 Star)": 4
};

// Create an empty line graph using Chart.js
const ctx = document.getElementById('sentimentChart').getContext('2d');
const sentimentChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],  // X-axis: Data points (e.g., timestamps)
        datasets: [{
            label: 'Sentiment Score',
            data: [],  // Y-axis: Sentiment values (0 to 4)
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            tension: 0.3, // Smooth curve
            pointRadius: 4,
        }]
    },
    options: {
        scales: {
            y: {
                min: 0,
                max: 4,
                ticks: {
                    stepSize: 1
                }
            }
        }
    }
});

// Function to update the sentiment graph dynamically
function updateSentimentGraph(sentimentLabel) {
    const sentimentValue = sentimentMap[sentimentLabel] ?? null;
    if (sentimentValue === null) return;

    const currentTime = new Date().toLocaleTimeString();  // Use timestamp for X-axis
    sentimentChart.data.labels.push(currentTime);
    sentimentChart.data.datasets[0].data.push(sentimentValue);

    if (sentimentChart.data.labels.length > 10) {
        sentimentChart.data.labels.shift();  // Remove oldest entry to keep graph readable
        sentimentChart.data.datasets[0].data.shift();
    }

    sentimentChart.update();
}
