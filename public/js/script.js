// Function to handle the form submission and get the prediction
async function getSentiment() {
    const text = document.getElementById('inputText').value;

    // Check if the input is not empty
    if (text.trim() === '') {
        alert('Please enter some text');
        return;
    }

    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });

    const result = await response.json();

    // Display the sentiment result
    document.getElementById('result').innerText = `Predicted Sentiment: ${result.sentiment}`;
}
