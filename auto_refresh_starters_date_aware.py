"""
Improved auto-refresh with date-aware storage structure to prevent historical data corruption
"""

import requests
import json
import os
from datetime import datetime, date

def fetch_and_update_starters_date_aware():
    """Fetch today's projected starters with date-aware storage structure"""
    print(f"🔄 Auto-refreshing projected starters with date-aware storage...")
    
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
        todays_starters = {}
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
                todays_starters[matchup_key] = {
                    'away_team': away_team,
                    'home_team': home_team,
                    'away_starter': away_starter,
                    'home_starter': home_starter,
                    'date': today,  # Add date metadata
                    'last_updated': datetime.now().isoformat()
                }
        
        games_found = len(todays_starters)
        print(f"✅ Found {games_found} games with correct date {today}")
        
        if games_with_wrong_date > 0:
            print(f"⚠️ Skipped {games_with_wrong_date} games with incorrect date")
        
        if games_found == 0:
            print(f"❌ No games found for {today} - this might indicate an off-day or API issue")
            return
        
        # Load existing data with date-aware structure
        starters_file = 'ProjectedStarters_DateAware.json'
        if os.path.exists(starters_file):
            try:
                with open(starters_file, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
            except Exception:
                all_data = {}
        else:
            all_data = {}
        
        # Ensure date structure exists
        if today not in all_data:
            all_data[today] = {}
        
        # Update with today's verified data
        all_data[today] = todays_starters
        
        # Also maintain legacy format for backward compatibility
        legacy_data = {}
        for date_key, date_games in all_data.items():
            if date_key == today:  # Only include today's games in legacy format
                legacy_data.update(date_games)
        
        # Save date-aware format
        with open(starters_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        # Save legacy format
        with open('ProjectedStarters.json', 'w', encoding='utf-8') as f:
            json.dump(legacy_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Updated ProjectedStarters_DateAware.json with {games_found} verified games for {today}")
        print(f"💾 Updated ProjectedStarters.json (legacy format) with {games_found} games")
        
        # Show sample matchups
        if games_found > 0:
            print("\n📋 Sample verified matchups:")
            for i, (matchup, data) in enumerate(list(todays_starters.items())[:3]):
                away_starter = data.get('away_starter', 'TBD')
                home_starter = data.get('home_starter', 'TBD')
                date_stored = data.get('date', 'Unknown')
                print(f"   {matchup} (Date: {date_stored})")
                print(f"     Away: {away_starter or 'TBD'}")
                print(f"     Home: {home_starter or 'TBD'}")
                
    except Exception as e:
        print(f"❌ Error fetching starters: {e}")

def show_date_aware_structure():
    """Display the current date-aware structure"""
    starters_file = 'ProjectedStarters_DateAware.json'
    if os.path.exists(starters_file):
        print(f"\n📊 Current date-aware structure in {starters_file}:")
        with open(starters_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for date_key in sorted(data.keys()):
            games_count = len(data[date_key])
            print(f"   {date_key}: {games_count} games")
            
            # Show sample for today
            if date_key == datetime.now().strftime('%Y-%m-%d'):
                sample_games = list(data[date_key].items())[:2]
                for matchup, details in sample_games:
                    print(f"     {matchup}")
                    print(f"       Away: {details.get('away_starter', 'TBD')}")
                    print(f"       Home: {details.get('home_starter', 'TBD')}")
    else:
        print(f"\n📊 No date-aware file found yet")

if __name__ == "__main__":
    fetch_and_update_starters_date_aware()
    show_date_aware_structure()
