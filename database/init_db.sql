-- Districts Metadata
CREATE TABLE IF NOT EXISTS districts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    state VARCHAR(50) DEFAULT 'Tamil Nadu',
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical Yield Data (Training Data)
CREATE TABLE IF NOT EXISTS historical_yield (
    id SERIAL PRIMARY KEY,
    district_id INTEGER REFERENCES districts(id),
    crop_name VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    season VARCHAR(20) NOT NULL, -- Kharif, Rabi, etc.
    yield_ton_per_acre DECIMAL(10, 2) NOT NULL,
    area_sown_acres DECIMAL(10, 2),
    UNIQUE(district_id, crop_name, year, season)
);

-- Weather and Soil Data (Features)
CREATE TABLE IF NOT EXISTS weather_soil_data (
    id SERIAL PRIMARY KEY,
    district_id INTEGER REFERENCES districts(id),
    record_date DATE NOT NULL,
    rainfall_mm DECIMAL(10, 2),
    temperature_min DECIMAL(5, 2),
    temperature_max DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    nitrogen_kgha DECIMAL(10, 2),
    phosphorus_kgha DECIMAL(10, 2),
    potassium_kgha DECIMAL(10, 2),
    ph_level DECIMAL(4, 2),
    UNIQUE(district_id, record_date)
);

-- Prediction Logs (Observability)
CREATE TABLE IF NOT EXISTS prediction_logs (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(50) NOT NULL, -- '/predict_yield' or '/disease_risk'
    input_data JSONB,
    prediction_result JSONB,
    processing_time_ms DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Initial Seed Data for Districts (Example)
INSERT INTO districts (name, latitude, longitude) VALUES 
('Thanjavur', 10.7870, 79.1378),
('Madurai', 9.9252, 78.1198),
('Coimbatore', 11.0168, 76.9558),
('Tiruchirappalli', 10.7905, 78.7047)
ON CONFLICT (name) DO NOTHING;
