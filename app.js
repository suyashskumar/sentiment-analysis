require('dotenv').config();  // Load environment variables from the .env file
const mysql = require('mysql2');
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

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
  
  if (!text || text.trim() === '') {
    return res.status(400).json({ error: 'Text input cannot be empty' });
  }

  try {
    const python = spawn('python', ['src/sentiment_model.py', text]);

    let sentiment = 'Unknown Sentiment';
    let feedback = 'No feedback available';

    python.stdout.on('data', (data) => {
      const output = data.toString().trim();
      console.log('Python output:', output);

      try {
        const result = JSON.parse(output);
        sentiment = result.sentiment_label || 'Unknown Sentiment';
        feedback = result.feedback || 'No feedback available';
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

      // Insert into sentiment_inputs table
      const query = 'INSERT INTO sentiment_inputs (input_text, sentiment_label, created_at) VALUES (?, ?, NOW())';
      connection.query(query, [text, sentiment], (err, result) => {
        if (err) {
          console.error('Error inserting data into the database:', err);
          return res.status(500).json({ error: 'Database insertion failed' });
        }
        console.log('Data inserted successfully:', result);
        
        // Send response after successful database insertion
        res.json({ sentiment, feedback });
      });
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Something went wrong' });
  }
});

// **History Route**
app.get('/history', (req, res) => {
  const query = `SELECT input_text, sentiment_label, created_at FROM sentiment_inputs ORDER BY created_at DESC`;

  connection.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching history:", err);
      return res.status(500).send("Database query failed");
    }
    res.render('history', { history: results });
  });
});

// **Custom Input Route**
app.get('/custom-input', (req, res) => {
  res.render('custom_input');
});

app.get('/brands', (req, res) => {
  res.render('brands');
});

app.post('/analyze', async (req, res) => {
  const { url } = req.body;

  if (!url || url.trim() === '') {
    return res.status(400).json({ error: 'URL cannot be empty' });
  }

  try {
    console.log(`Scraping data from: ${url}`);

    // Step 1: Spawn the Python scraper
    const scraper = spawn('python', ['src/webscraper.py', url]);

    scraper.stderr.on('data', (data) => {
      console.error(`Scraper stderr: ${data}`);
    });

    scraper.on('close', (code) => {
      if (code !== 0) {
        return res.status(500).json({ error: 'Scraping process failed' });
      }

      console.log('Scraping complete, starting sentiment analysis...');

      // Step 2: Run sentiment analysis (which generates the graph)
      const analyzer = spawn('python', ['src/sentiment_model2.py', 'batch']);

      let analysisResult = '';

      analyzer.stdout.on('data', (data) => {
        analysisResult += data.toString();
      });

      analyzer.stderr.on('data', (data) => {
        console.error(`Analyzer stderr: ${data}`);
      });

      analyzer.on('close', (code) => {
        if (code !== 0) {
          return res.status(500).json({ error: 'Sentiment analysis failed' });
        }

        console.log('Sentiment analysis complete. Graph generated.');

        // Fixed path to the graph
        const graphImageUrl = '/sentiment_distribution.png';
        const analysisFilePath = path.join(__dirname, 'public', 'analysis.txt');

        fs.readFile(analysisFilePath, 'utf8', (err, analysisSummary) => {
          if (err) {
            console.error('Error reading analysis.txt:', err);
            return res.status(500).json({ error: 'Failed to retrieve analysis summary' });
          }

          res.json({
            analysis_summary: analysisSummary.trim(), // Send only the file contents, not stdout
            graph_url: graphImageUrl,
          });
        });
      });
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Something went wrong' });
  }
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});