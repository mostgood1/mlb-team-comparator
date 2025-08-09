#!/usr/bin/env python3
"""
Diagnostic script to check what data is missing from the API response
"""

import json
import sys
import os

# Add the current directory to the path
sys.path.append(os.getcwd())

try:
    from app import app
    from TodaysGames import TodaysGames
    from cumulative_ultra_fast_engine import CumulativeUltraFastEngine
    import ultra_fast_engine
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def diagnose_missing_data():
    """Check what data is available vs what's missing"""
    print("🔍 DIAGNOSING MISSING DATA ISSUES")
    print("=" * 50)
    
    # 1. Check if we can get today's games
    print("\n1️⃣ CHECKING GAME DATA:")
    try:
        todays_games = TodaysGames()
        games = todays_games.get_games_for_date("2025-08-09")
        print(f"   ✅ Found {len(games)} games for today")
        
        if games:
            first_game = games[0]
            print(f"   📝 Sample game structure:")
            for key, value in first_game.items():
                print(f"      - {key}: {type(value)} = {value}")
        else:
            print("   ❌ No games found!")
            
    except Exception as e:
        print(f"   ❌ Error getting games: {e}")
    
    # 2. Check pitcher data
    print("\n2️⃣ CHECKING PITCHER DATA:")
    try:
        with open('ProjectedStarters.json', 'r') as f:
            pitcher_data = json.load(f)
        
        print(f"   ✅ Loaded pitcher data for {len(pitcher_data)} matchups")
        
        if pitcher_data:
            first_matchup = list(pitcher_data.values())[0]
            print(f"   📝 Sample pitcher structure:")
            for key, value in first_matchup.items():
                print(f"      - {key}: {value}")
                
    except Exception as e:
        print(f"   ❌ Error loading pitcher data: {e}")
    
    # 3. Check prediction engine response
    print("\n3️⃣ CHECKING PREDICTION ENGINE:")
    try:
        engine = CumulativeUltraFastEngine()
        prediction = engine.get_cumulative_prediction("MIA", "ATL")
        
        print(f"   ✅ Prediction engine working")
        print(f"   📝 Sample prediction structure:")
        for key, value in prediction.items():
            if isinstance(value, dict):
                print(f"      - {key}: (dict with {len(value)} keys)")
                for subkey, subvalue in value.items():
                    print(f"        └─ {subkey}: {subvalue}")
            else:
                print(f"      - {key}: {value}")
                
    except Exception as e:
        print(f"   ❌ Error with prediction engine: {e}")
    
    # 4. Check team stats/win percentages
    print("\n4️⃣ CHECKING TEAM STATS & WIN PERCENTAGES:")
    try:
        from ultra_fast_engine import UltraFastEngine
        base_engine = UltraFastEngine()
        
        # Check if team stats are available
        if hasattr(base_engine, 'team_stats'):
            print(f"   ✅ Team stats available: {len(base_engine.team_stats)} teams")
            
            sample_team = list(base_engine.team_stats.keys())[0]
            sample_stats = base_engine.team_stats[sample_team]
            print(f"   📝 Sample team stats for {sample_team}:")
            for key, value in sample_stats.items():
                print(f"      - {key}: {value}")
        else:
            print("   ❌ No team_stats attribute found")
            
    except Exception as e:
        print(f"   ❌ Error checking team stats: {e}")
    
    # 5. Check what the API endpoint actually returns
    print("\n5️⃣ TESTING API ENDPOINT:")
    try:
        with app.test_client() as client:
            response = client.get('/api/fast-predictions')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✅ API response successful ({response.status_code})")
                print(f"   📝 Response structure:")
                
                if 'predictions' in data and data['predictions']:
                    first_prediction = data['predictions'][0]
                    print(f"      - Found {len(data['predictions'])} predictions")
                    print(f"      - Sample prediction keys: {list(first_prediction.keys())}")
                    
                    # Check for specific missing data
                    missing_fields = []
                    expected_fields = ['away_team', 'home_team', 'predictions', 'pitcher_quality']
                    
                    for field in expected_fields:
                        if field not in first_prediction:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f"      ❌ Missing fields: {missing_fields}")
                    else:
                        print(f"      ✅ All expected fields present")
                        
                    # Check pitcher_quality specifically
                    if 'pitcher_quality' in first_prediction:
                        pq = first_prediction['pitcher_quality']
                        if pq:
                            print(f"      📝 Pitcher quality keys: {list(pq.keys())}")
                        else:
                            print(f"      ❌ pitcher_quality is empty/None")
                    
                else:
                    print(f"      ❌ No predictions in response")
                    print(f"      📝 Response keys: {list(data.keys())}")
            else:
                print(f"   ❌ API error: {response.status_code}")
                print(f"   📝 Response: {response.get_data()}")
                
    except Exception as e:
        print(f"   ❌ Error testing API: {e}")
    
    print("\n🎯 DIAGNOSIS COMPLETE")
    print("Check the output above to identify what data is missing!")

if __name__ == "__main__":
    diagnose_missing_data()
