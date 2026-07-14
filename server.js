const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.static('public'));

// Quran API endpoints
const QURAN_API = 'https://api.alquran.cloud/v1';

// Get all surahs (chapters)
app.get('/api/surahs', async (req, res) => {
  try {
    const response = await axios.get(`${QURAN_API}/surah`);
    res.json(response.data.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch surahs' });
  }
});

// Get surah by number with translations
app.get('/api/surah/:number', async (req, res) => {
  try {
    const { number } = req.params;
    
    // Fetch Arabic text
    const arabicRes = await axios.get(`${QURAN_API}/surah/${number}`);
    
    // Fetch English translation (Sahih International)
    const englishRes = await axios.get(`${QURAN_API}/surah/${number}/editions/quran-uthmani,en.sahih`);
    
    res.json({
      surah: arabicRes.data.data,
      editions: englishRes.data.data
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch surah' });
  }
});

// Search ayahs
app.get('/api/search', async (req, res) => {
  try {
    const { q } = req.query;
    if (!q) {
      return res.status(400).json({ error: 'Query required' });
    }
    
    const response = await axios.get(`${QURAN_API}/search?query=${encodeURIComponent(q)}`);
    res.json(response.data.data);
  } catch (error) {
    res.status(500).json({ error: 'Search failed' });
  }
});

app.listen(PORT, () => {
  console.log(`Quran app running on http://localhost:${PORT}`);
});
