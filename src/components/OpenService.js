// src/openrouterService.js
import axios from 'axios';

const API_KEY = '<Paste you API key here>'; // Replace with your key

export const getAICompletion = async (userInput) => {
  const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
    // Optional:
    'HTTP-Referer': 'https://your-site.com',
    'X-Title': 'Your App Name'
  };

  const body = {
    model: 'deepseek/deepseek-r1:free',
    messages: [
      { role: 'user', content: userInput }
    ]
  };

  const response = await axios.post(
    'https://openrouter.ai/api/v1/chat/completions',
    body,
    { headers }
  );

  // Adapt this based on the exact JSON response structure:
  return response.data.choices[0].message.content;
};
