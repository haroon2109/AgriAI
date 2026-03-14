import sqlite3
import os

DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "ndvi_cache.db")

def init_db():
    """Initializes the SQLite cache database for NDVI/EVI coordinates."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lat_lon_cache (
            lat REAL,
            lon REAL,
            ndvi REAL,
            evi REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (lat, lon)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[INFO] SQLite database initialized at {DB_PATH}")

def get_cached_indices(lat, lon, tolerance=0.01):
    """
    Checks if there's a cached NDVI/EVI value nearby (within tolerance deg).
    Returns (ndvi, evi) or None.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Simple bounding box query
    cursor.execute('''
        SELECT ndvi, evi FROM lat_lon_cache
        WHERE lat BETWEEN ? AND ? AND lon BETWEEN ? AND ?
        ORDER BY last_updated DESC LIMIT 1
    ''', (lat - tolerance, lat + tolerance, lon - tolerance, lon + tolerance))
    
    row = cursor.fetchone()
    conn.close()
    
    return row if row else None

def set_cached_indices(lat, lon, ndvi, evi):
    """Saves or updates the cache for a given coord."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO lat_lon_cache (lat, lon, ndvi, evi)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(lat, lon) DO UPDATE SET
            ndvi = excluded.ndvi,
            evi = excluded.evi,
            last_updated = CURRENT_TIMESTAMP
    ''', (lat, lon, ndvi, evi))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
