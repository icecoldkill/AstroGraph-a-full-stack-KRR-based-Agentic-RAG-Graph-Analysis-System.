const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5001;
const PYTHON_BRIDGE_URL = process.env.PYTHON_BRIDGE_URL || 'http://localhost:8000';

app.use(cors());
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.json({ status: "Space Explorer API Gateway Online", version: "3.1" });
});

// Routes
app.get('/api/status', (req, res) => {
    res.json({ message: 'Node.js Backend Active' });
});

// Proxy to Python KRR Bridge
app.post('/api/krr/query', async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_BRIDGE_URL}/query`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/krr/graph', async (req, res) => {
    try {
        const response = await axios.get(`${PYTHON_BRIDGE_URL}/graph/summary`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Proxy to Python KRR Bridge for Chat/Agent
app.post('/api/chat', async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_BRIDGE_URL}/chat`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// SPARQL Endpoint Proxies
app.post('/api/sparql', async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_BRIDGE_URL}/sparql`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/sparql/queries', async (req, res) => {
    try {
        const response = await axios.get(`${PYTHON_BRIDGE_URL}/sparql/queries`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/sparql/query/:queryId', async (req, res) => {
    try {
        const queryId = req.params.queryId;
        const response = await axios.get(`${PYTHON_BRIDGE_URL}/sparql/query/${queryId}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Dynamic KRR Upload Handler
const multer = require('multer');
const FormData = require('form-data');
const fs = require('fs');
const upload = multer({ dest: 'uploads/' });

app.post('/api/upload', upload.single('file'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }
    try {
        const formData = new FormData();
        formData.append('file', fs.createReadStream(req.file.path));

        // Send to Python Worker
        const response = await axios.post(`${PYTHON_BRIDGE_URL}/upload_and_process`, formData, {
            headers: { ...formData.getHeaders() }
        });

        fs.unlinkSync(req.file.path); // Cleanup
        res.json(response.data);
    } catch (error) {
        console.error("Upload Bridge Error:", error.message);
        res.status(500).json({ error: 'KRR Processing Failed' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
