const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
app.set('view engine', 'ejs');  // Use EJS for rendering
app.set('views', path.join(__dirname, 'views')); // This should be at the root level
app.use(express.static(path.join(__dirname, 'public')));  // Serve static files from 'public' folder
app.use(bodyParser.json());      // Parse JSON bodies

// Serve the index page
app.get('/', (req, res) => {
    res.render('index');  // Ensure 'index.ejs' is in the 'views' directory at the root level
});

// /predict endpoint to receive input text and return sentiment and feedback
app.post('/predict', (req, res) => {
    const { text } = req.body;  // Get text from the request body

    try {
        const python = spawn('python', ['src/sentiment_model.py', text]);

        let sentiment = '';  // Store the sentiment prediction
        let feedback = '';  // Store the generated feedback
        python.stdout.on('data', (data) => {
            const output = data.toString().trim();
            // We expect the first line to be sentiment, second to be feedback
            const [sentimentLine, feedbackLine] = output.split('\n');
            sentiment = sentimentLine;
            feedback = feedbackLine || '';
        });

        python.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        python.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({ error: 'Python process failed' });
            }

            console.log('Sentiment Value:', sentiment);

            // Send both sentiment and feedback in the response
            res.json({ sentiment, feedback });
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Something went wrong' });
    }
});

// Start the server on port 3000
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});