-- Enable PostGIS Extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Districts with Geometry
CREATE TABLE IF NOT EXISTS districts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    state VARCHAR(50) DEFAULT 'Tamil Nadu',
    geom GEOMETRY(MultiPolygon, 4326),  -- Storing shape boundaries
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crop Yield Forecasts
CREATE TABLE IF NOT EXISTS yield_forecasts (
    id SERIAL PRIMARY KEY,
    district_id INTEGER REFERENCES districts(id),
    crop_name VARCHAR(50) NOT NULL,
    predicted_yield DECIMAL(10, 2),
    forecast_date DATE DEFAULT CURRENT_DATE
);

-- Disease Risk Scores
CREATE TABLE IF NOT EXISTS disease_risk (
    id SERIAL PRIMARY KEY,
    district_id INTEGER REFERENCES districts(id),
    risk_level VARCHAR(20),     -- Low, Medium, High
    risk_score DECIMAL(5, 4),   -- 0.0 to 1.0 probability
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for Spatial Queries
CREATE INDEX idx_districts_geom ON districts USING GIST (geom);
