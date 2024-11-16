const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios'); // For making HTTP requests
const app = express();

app.use(bodyParser.json());
app.use(cors());

// Helper function to call Tune AI API
const callTuneAI = async (prompt) => {
    const url = "https://proxy.tune.app/chat/completions";
    
    // Double-check that all the fields are properly formatted and aligned with API expectations
    const payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an academic tutor for a programming languages and compilers college course"
            },
            {
                "role": "user",
                "content": prompt // This will be the comparison text
            }
        ],
        "model": "NLNHSR-llama3-1-8b", // Make sure this model is valid and available
        "max_tokens": 123,  // Adjust as needed depending on API limits
        "temperature": 1.0, // Ensure this is the expected value
        "top_p": 1.0, // Defaulting to 1.0, modify based on API spec
        "n": 1 // Only one completion
    };

    const headers = {
        "X-Org-Id": "0266c7a8-a772-47c1-a450-b02275131dc7",
        "Authorization": "Bearer sk-tune-nBUsrB2PKHYgYu98pLUG3sTmIDpSkegHzis",
        "Content-Type": "application/json"
    };

    try {
        // Send the request to the Tune AI API
        const response = await axios.post(url, payload, { headers });
        return response.data; // Return the response data from Tune API
    } catch (error) {
        console.error('Tune AI API error:', error.response ? error.response.data : error.message);
        throw new Error('Failed to fetch response from Tune AI API');
    }
};


// Route to handle embedding comparisons
app.post('/compare_embeddings', async (req, res) => {
    const { word1, word2 } = req.body;

    // Construct the prompt
    const prompt = `Compare the following two words:\n\nWord 1: ${word1}\nWord 2: ${word2}`;

    try {
        // Call Tune AI API with the constructed prompt
        const tuneAIResponse = await callTuneAI(prompt);
        res.send(tuneAIResponse);
    } catch (apiError) {
        console.error(apiError);
        res.status(500).send('Error calling Tune AI API');
    }
});

// Start the server
const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
