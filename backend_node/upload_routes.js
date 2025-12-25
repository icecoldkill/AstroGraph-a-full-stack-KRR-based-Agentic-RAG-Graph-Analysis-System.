const multer = require('multer');
const FormData = require('form-data');
const fs = require('fs');
const upload = multer({ dest: 'uploads/' });

// Document Upload Endpoint for Dynamic KRR
app.post('/api/upload', upload.single('file'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    try {
        const formData = new FormData();
        formData.append('file', fs.createReadStream(req.file.path));

        const response = await axios.post(`${PYTHON_BRIDGE_URL}/upload_and_process`, formData, {
            headers: {
                ...formData.getHeaders()
            }
        });

        // Cleanup temp file
        fs.unlinkSync(req.file.path);

        res.json(response.data);
    } catch (error) {
        console.error("Upload error:", error.message);
        res.status(500).json({ error: 'Failed to process document in KRR engine.' });
    }
});
