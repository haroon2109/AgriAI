-- AgriAI "MNC Standard" Database Schema
-- Optimized for Scalability on Supabase / PostgreSQL

-- 1. Users Table (Profile Management)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    district VARCHAR(50),
    soil_type VARCHAR(50), -- e.g., 'Red Loam', 'Clay'
    primary_crop VARCHAR(50), -- e.g., 'Paddy', 'Tomato'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE
);

-- 2. Crop Scans (Historical Health Tracking)
CREATE TABLE crop_scans (
    scan_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    image_url TEXT NOT NULL, -- S3 / Cloudinary URL
    disease_detected VARCHAR(100),
    confidence_score FLOAT,
    location_lat FLOAT,
    location_long FLOAT,
    scan_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expert_verified BOOLEAN DEFAULT FALSE
);

-- 3. Market Cache (Fast Loading & Offline Support)
-- Stores Mandi prices to avoid frequent API calls to Agmarknet
CREATE TABLE market_cache (
    cache_id SERIAL PRIMARY KEY,
    mandi_name VARCHAR(100),
    commodity VARCHAR(100),
    price_min DECIMAL(10,2),
    price_max DECIMAL(10,2),
    modal_price DECIMAL(10,2),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Community Voice ("Digital Thinnai")
-- Stores audio URLs and transcribed text for forum posts
CREATE TABLE community_voice (
    post_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    audio_url TEXT NOT NULL,
    transcribed_text TEXT, -- Output from Whisper
    sentiment VARCHAR(20), -- 'Positive', 'Urgent', 'Query'
    location_tag VARCHAR(50),
    upvotes INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for fast searching by location (MNC Performance Standard)
CREATE INDEX idx_users_district ON users(district);
CREATE INDEX idx_market_mandi ON market_cache(mandi_name);
