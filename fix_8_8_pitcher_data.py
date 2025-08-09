#!/usr/bin/env python3
"""
Recover accurate 8/8/2025 pitcher data to fix historical accuracy
"""

import requests
import json
from datetime import datetime

def fetch_historical_pitcher_data(date_str):
    """Fetch pitcher data for a specific historical date from MLB API"""
    print(f"🔍 Fetching pitcher data for {date_str}...")
    
    try:
        # Get the game schedule for this date
        schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&hydrate=probablePitcher,team"
        
        response = requests.get(schedule_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        games = data.get('dates', [{}])[0].get('games', [])
        pitcher_data = {}
        
        print(f"📊 Found {len(games)} games for {date_str}")
        
        for game in games:
            try:
                # Extract team info
                away_team_info = game.get('teams', {}).get('away', {}).get('team', {})
                home_team_info = game.get('teams', {}).get('home', {}).get('team', {})
                
                away_team = away_team_info.get('name', '')
                home_team = home_team_info.get('name', '')
                
                # Extract pitcher info
                away_pitcher_info = game.get('teams', {}).get('away', {}).get('probablePitcher')
                home_pitcher_info = game.get('teams', {}).get('home', {}).get('probablePitcher')
                
                away_pitcher = 'TBD'
                home_pitcher = 'TBD'
                
                if away_pitcher_info:
                    away_pitcher = away_pitcher_info.get('fullName', 'TBD')
                
                if home_pitcher_info:
                    home_pitcher = home_pitcher_info.get('fullName', 'TBD')
                
                # Create matchup key
                matchup_key = f"{away_team} at {home_team}"
                
                pitcher_data[matchup_key] = {
                    "away_team": away_team,
                    "home_team": home_team,
                    "away_starter": away_pitcher,
                    "home_starter": home_pitcher,
                    "date": date_str,
                    "last_updated": datetime.now().isoformat()
                }
                
                print(f"✅ {matchup_key}: {away_pitcher} vs {home_pitcher}")
                
            except Exception as e:
                print(f"⚠️  Error processing game: {e}")
                continue
        
        return pitcher_data
        
    except Exception as e:
        print(f"❌ Error fetching data for {date_str}: {e}")
        return {}

def update_date_aware_storage(date_str, pitcher_data):
    """Add the historical data to the date-aware storage"""
    try:
        # Load existing date-aware data
        try:
            with open('ProjectedStarters_DateAware.json', 'r') as f:
                date_aware_data = json.load(f)
        except FileNotFoundError:
            date_aware_data = {}
        
        # Add the historical date data
        date_aware_data[date_str] = pitcher_data
        
        # Save back to file
        with open('ProjectedStarters_DateAware.json', 'w') as f:
            json.dump(date_aware_data, f, indent=2)
        
        print(f"✅ Updated DateAware storage with {len(pitcher_data)} games for {date_str}")
        
    except Exception as e:
        print(f"❌ Error updating DateAware storage: {e}")

def fix_8_8_pitcher_data():
    """Main function to fix the 8/8 pitcher data issue"""
    print("🔧 FIXING 8/8/2025 PITCHER DATA ACCURACY")
    print("=" * 50)
    
    target_date = "2025-08-08"
    
    # Fetch the correct historical data
    correct_pitcher_data = fetch_historical_pitcher_data(target_date)
    
    if correct_pitcher_data:
        print(f"\n📝 CORRECT 8/8 PITCHER DATA RECOVERED:")
        for matchup, data in correct_pitcher_data.items():
            print(f"   ✅ {matchup}")
            print(f"      Away: {data['away_starter']}")
            print(f"      Home: {data['home_starter']}")
        
        # Update the date-aware storage
        update_date_aware_storage(target_date, correct_pitcher_data)
        
        # Also create a backup file specifically for 8/8
        backup_filename = f"ProjectedStarters_8_8_2025_CORRECTED.json"
        with open(backup_filename, 'w') as f:
            json.dump(correct_pitcher_data, f, indent=2)
        
        print(f"\n✅ BACKUP CREATED: {backup_filename}")
        print(f"✅ DATE-AWARE STORAGE UPDATED")
        print(f"🎯 8/8 pitcher data now historically accurate!")
        
    else:
        print("❌ Could not fetch 8/8 pitcher data - may need manual correction")

if __name__ == "__main__":
    fix_8_8_pitcher_data()
