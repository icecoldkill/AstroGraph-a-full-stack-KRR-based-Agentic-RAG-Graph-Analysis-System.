-- Final Project KRR Database Schema

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Missions Table (Metadata from KG)
CREATE TABLE IF NOT EXISTS missions (
    id SERIAL PRIMARY KEY,
    external_id TEXT UNIQUE, -- mission_1, mission_2 etc.
    name TEXT NOT NULL,
    agency TEXT,
    budget FLOAT,
    status TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Graph Meta Table (Hashing & Versioning)
CREATE TABLE IF NOT EXISTS graph_states (
    id SERIAL PRIMARY KEY,
    hash_value TEXT NOT NULL,
    compressed_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Initial Data (Optional)
INSERT INTO missions (external_id, name, agency, budget, status) VALUES 
('mission_1', 'Apollo 11', 'NASA', 25000, 'Success')
ON CONFLICT (external_id) DO NOTHING;
