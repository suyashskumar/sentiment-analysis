require('dotenv').config();  // Load environment variables from the .env file
const mysql = require('mysql2');
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to the database:', err.stack);
    return;
  }
  console.log('Connected to the database');
});

app.get('/', (req, res) => {
  res.render('index');
});

app.post('/predict', (req, res) => {
    const { text } = req.body;
  
    try {
      const python = spawn('python', ['src/sentiment_model.py', text]);
  
      let sentiment = '';
      let feedback = '';
  
      python.stdout.on('data', (data) => {
        const output = data.toString().trim();
        console.log('Python output:', output);
  
        try {
          // Assuming the output is now a JSON string with both sentiment and feedback
          const result = JSON.parse(output);
          sentiment = result.sentiment_label;
          feedback = result.feedback;
        } catch (error) {
          console.error('Error parsing Python output:', error);
        }
      });
  
      python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
      });
  
      python.on('close', (code) => {
        if (code !== 0) {
          return res.status(500).json({ error: 'Python process failed' });
        }
  
        console.log('Sentiment:', sentiment);
        console.log('Feedback:', feedback);
  
        // Insert only input_text and sentiment_label into the database
        const query = 'INSERT INTO sentiment_inputs (input_text, sentiment_label) VALUES (?, ?)';
        connection.query(query, [text, sentiment], (err, result) => {
          if (err) {
            console.error('Error inserting data into the database:', err);
            return res.status(500).json({ error: 'Database insertion failed' });
          }
          console.log('Data inserted successfully:', result);
        });
  
        // Return the sentiment and feedback as JSON response
        res.json({ sentiment, feedback });
      });
  
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Something went wrong' });
    }
  }); 

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});