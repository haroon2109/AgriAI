import requests
import pandas as pd
import datetime

# --- CONFIG ---
API_KEY = "YOUR_OGD_API_KEY"  # Register at data.gov.in
RESOURCE_ID = "9ef842fd-9a74-4c2a-8488-39415051479d" # Verify this on data.gov.in

def fetch_tn_market_prices(api_key=API_KEY):
    """
    Fetches daily market prices for Tamil Nadu from OGD India API.
    """
    url = f"https://api.data.gov.in/resource/{resource_id}?api-key={api_key}&format=json&filters[state]=Tamil+Nadu&limit=1000"

    try:
        response = requests.get(url)
        data = response.json()
        
        records = data.get('records', [])
        df = pd.DataFrame(records)

        if df.empty:
            print("No data found from API.")
            return None

        # Cleaning
        price_cols = ['min_price', 'max_price', 'modal_price']
        for col in price_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['arrival_date'] = pd.to_datetime(df['arrival_date'], dayfirst=True)
        str_cols = ['district', 'market', 'commodity', 'variety']
        for col in str_cols:
            df[col] = df[col].str.strip()

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_price_signal(current_price, historical_avg, arrivals_trend):
    """
    Cultural Price Compass Logic (விலை திசைகாட்டி)
    Returns: Signal (SELL/WAIT/STABLE), Message (Tamil)
    """
    # Logic 1: High Price + High Supply -> Sell Fast
    if current_price > (historical_avg * 1.15) and arrivals_trend == 'increasing':
        return "🔴 SELL NOW (விற்கவும்)", "விலை உச்சத்தில் உள்ளது. வரத்து அதிகரிப்பதால் விலை குறையலாம்."

    # Logic 2: Low Price + Low Supply -> Hold
    elif current_price < historical_avg and arrivals_trend == 'decreasing':
        return "🟢 WAIT (காத்திருக்கவும்)", "விலை குறைவாக உள்ளது. வரத்து குறைவதால் விரைவில் விலை உயரலாம்."

    else:
        return "🟡 STABLE (சீரானது)", "விலை சீராக உள்ளது. தேவைக்கேற்ப விற்கலாம்."

# --- MOCK EXECUTION FOR DEMO ---
if __name__ == "__main__":
    print("--- AgriAI Market Backend ---")
    
    # Simulating data for Thanjavur
    print("Fetching data for Thanjavur...")
    # df = fetch_tn_market_prices() 
    # Mocking DF for demonstration since we don't have a real API Key in this env
    
    test_price = 2400
    avg_price = 2100
    trend = 'increasing'
    
    signal, msg = get_price_signal(test_price, avg_price, trend)
    print(f"\nSimulation Result for Paddy:")
    print(f"Current Price: ₹{test_price} | Signal: {signal}")
    print(f"Advice: {msg}")
