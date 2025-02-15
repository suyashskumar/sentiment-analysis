// Auto-resize textarea based on input
function resizeTextarea() {
    const textarea = document.getElementById('inputText');
    textarea.style.height = 'auto';  // Reset height to recalculate it
    textarea.style.height = `${textarea.scrollHeight}px`;  // Adjust height dynamically
}

// Function to handle single sentiment analysis request
async function getSentiment() {
    const textarea = document.getElementById('inputText');
    if (!textarea) {
        alert('Text input field not found!');
        return;
    }

    const text = textarea.value.trim();
    const resultElement = document.getElementById('result');

    if (!text) {
        alert('Please enter some text.');
        return;
    }

    resultElement.innerText = 'Analyzing sentiment...';
    resultElement.className = 'loading'; 

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            const errorData = await response.text();  // Get server error message
            throw new Error(`Server Error: ${errorData}`);
        }

        const { sentiment, feedback } = await response.json();
        console.log('Sentiment:', sentiment);
        console.log('Feedback:', feedback);

        resultElement.innerHTML = `<strong>Predicted Sentiment:</strong> ${sentiment} <br><br>
                                   <strong>Analysis & Feedback:</strong> <br>${feedback}`;
        updateSentimentClass(resultElement, sentiment);
    } catch (error) {
        console.error('Error:', error);
        resultElement.innerText = `Error occurred: ${error.message}`;
        resultElement.className = 'error';
    }
}


// Function to handle bulk sentiment analysis request
async function analyzeSentiment() {
    const url = document.getElementById('urlInput').value.trim();
    const resultElement = document.getElementById('result');
    const feedbackElement = document.getElementById('analysisText');
    const graphImage = document.getElementById('sentimentGraph'); // Reference to graph image

    if (!url) {
        alert('Please enter a URL.');
        return;
    }

    resultElement.innerText = 'Collecting data...';
    resultElement.className = 'loading'; 

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url }),
        });

        if (!response.ok) {
            const errorData = await response.text();
            throw new Error(`Server Error: ${errorData}`);
        }

        const analysisResults = await response.json();

        feedbackElement.innerHTML = `<strong>Analysis & Feedback:</strong> <br>${analysisResults.analysis_summary}`;
        resultElement.innerText = 'Analysis Complete!';
        resultElement.classList.remove('loading');

        // ✅ Force browser to fetch new image (append timestamp)
        graphImage.src = `/sentiment_distribution.png?t=${new Date().getTime()}`;
        graphImage.style.display = 'block'; // Ensure it's visible
    } catch (error) {
        console.error('Error:', error);
        resultElement.innerText = `Error occurred: ${error.message}`;
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

/** ======= Line Graph for Sentiment Trends (UPDATED) ======= **/
const sentimentMap = {
    "Extremely Negative (1 Star)": 0,
    "Slightly Negative (2 Star)": 1,
    "Neutral (3 Star)": 2,
    "Slightly Positive (4 Star)": 3,
    "Extremely Positive (5 Star)": 4
};

const ctx = document.getElementById('sentimentChart').getContext('2d');
const sentimentChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Sentiment Score',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            tension: 0.3,
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

    const currentTime = new Date().toLocaleTimeString();
    sentimentChart.data.labels.push(currentTime);
    sentimentChart.data.datasets[0].data.push(sentimentValue);

    if (sentimentChart.data.labels.length > 10) {
        sentimentChart.data.labels.shift();
        sentimentChart.data.datasets[0].data.shift();
    }

    sentimentChart.update();
}