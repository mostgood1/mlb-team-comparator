"""
Enhanced auto-refresh with date verification to prevent future pitcher data
"""

import requests
import json
import os
from datetime import datetime, date

def fetch_and_update_starters_with_verification():
    """Fetch today's projected starters with date verification to prevent future data"""
    print(f"🔄 Auto-refreshing projected starters with date verification...")
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch from MLB API
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=probablePitcher,team,linescore"
    
    try:
        print(f"📡 Fetching data for {today}...")
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        
        # Parse the data with date verification
        starters = {}
        starters[today] = {}
        games_with_wrong_date = 0
        
        for date_obj in data.get('dates', []):
            api_date = date_obj.get('date', '')
            print(f"📅 API returned date: {api_date} (requested: {today})")
            
            if api_date != today:
                print(f"⚠️ Warning: API returned {api_date} data when {today} was requested")
                games_with_wrong_date += len(date_obj.get('games', []))
                continue  # Skip games from wrong date
            
            for game in date_obj.get('games', []):
                # Verify game date
                game_date = game.get('gameDate', '')[:10]  # Extract YYYY-MM-DD from ISO datetime
                if game_date != today:
                    print(f"⚠️ Skipping game with date {game_date} (expected {today})")
                    games_with_wrong_date += 1
                    continue
                
                away_team = game['teams']['away']['team']['name']
                home_team = game['teams']['home']['team']['name']
                away_starter = game['teams']['away'].get('probablePitcher', {}).get('fullName')
                home_starter = game['teams']['home'].get('probablePitcher', {}).get('fullName')
                
                matchup_key = f"{away_team} at {home_team}"
                starters[today][matchup_key] = {
                    'away_team': away_team,
                    'home_team': home_team,
                    'away_starter': away_starter,
                    'home_starter': home_starter
                }
        
        games_found = len(starters[today])
        print(f"✅ Found {games_found} games with correct date {today}")
        
        if games_with_wrong_date > 0:
            print(f"⚠️ Skipped {games_with_wrong_date} games with incorrect date")
        
        if games_found == 0:
            print(f"❌ No games found for {today} - this might indicate an off-day or API issue")
            return
        
        # Load existing data
        starters_file = 'ProjectedStarters.json'
        if os.path.exists(starters_file):
            try:
                with open(starters_file, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
            except Exception:
                all_data = {}
        else:
            all_data = {}
        
        # Update with today's data (flatten the structure)
        all_data.update(starters[today])
        
        # Save back to file
        with open(starters_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Updated ProjectedStarters.json with {games_found} verified games for {today}")
        
        # Show sample matchups
        if games_found > 0:
            print("\n📋 Sample verified matchups:")
            for i, (matchup, data) in enumerate(list(starters[today].items())[:3]):
                away_starter = data.get('away_starter', 'TBD')
                home_starter = data.get('home_starter', 'TBD')
                print(f"   {matchup}")
                print(f"     Away: {away_starter or 'TBD'}")
                print(f"     Home: {home_starter or 'TBD'}")
                
    except Exception as e:
        print(f"❌ Error fetching starters: {e}")

if __name__ == "__main__":
    fetch_and_update_starters_with_verification()
