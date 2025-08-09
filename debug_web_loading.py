"""
Debug web interface loading issue
"""
from app import app

# Test the main page and API
with app.test_client() as client:
    print("🌐 Testing main page")
    response = client.get('/')
    print(f"Main page status: {response.status_code}")
    
    print("\n🔍 Testing API endpoint")
    api_response = client.get('/api/fast-predictions')
    print(f"API status: {api_response.status_code}")
    
    if api_response.status_code == 200:
        data = api_response.get_json()
        if data and 'predictions' in data:
            print(f"✅ API working: {len(data['predictions'])} games found")
            print(f"📅 Date: {data.get('games_date', 'Unknown')}")
            
            # Show first game as sample
            if data['predictions']:
                first_game = data['predictions'][0]
                away = first_game.get('away_team', 'Unknown')
                home = first_game.get('home_team', 'Unknown')
                print(f"📊 Sample game: {away} @ {home}")
                
        elif data and 'error' in data:
            print(f"❌ API error: {data['error']}")
        else:
            print("❌ Unexpected API response format")
            print(f"Response keys: {list(data.keys()) if data else 'None'}")
    else:
        print(f"❌ API failed with status {api_response.status_code}")

print("\n🔧 Testing direct function calls")
try:
    from ultra_fast_engine import FastPredictionEngine
    engine = FastPredictionEngine()
    print("✅ Engine loads successfully")
    
    import TodaysGames
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    games = TodaysGames.get_games_for_date(today)
    print(f"✅ TodaysGames working: {len(games)} games for {today}")
    
except Exception as e:
    print(f"❌ Direct function error: {e}")
