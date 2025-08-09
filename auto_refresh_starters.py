#!/usr/bin/env python3
"""
Auto-Refresh Projected Starters
Fetches today's probable pitchers and updates the ProjectedStarters.json file
"""

import requests
from datetime import datetime
import json
import os

def fetch_and_update_starters():
    """Fetch today's projected starters and update the JSON file"""
    
    print(f"🔄 Auto-refreshing projected starters...")
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch from MLB API
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=probablePitcher,team,linescore"
    
    try:
        print(f"📡 Fetching data for {today}...")
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        
        # Parse the data
        starters = {}
        starters[today] = {}
        
        for date in data.get('dates', []):
            for game in date.get('games', []):
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
        print(f"✅ Found {games_found} games with projected starters")
        
        # Load existing data
        starters_file = 'ProjectedStarters.json'
        if os.path.exists(starters_file):
            with open(starters_file, 'r', encoding='utf-8') as f:
                try:
                    all_data = json.load(f)
                except Exception:
                    all_data = {}
        else:
            all_data = {}
        
        # Update with today's data
        all_data.update(starters)
        
        # Save back to file
        with open(starters_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Updated ProjectedStarters.json with {games_found} games for {today}")
        
        # Show sample matchups
        if games_found > 0:
            print("\n📋 Sample matchups:")
            for i, (matchup, data) in enumerate(list(starters[today].items())[:3]):
                away_starter = data.get('away_starter', 'TBD')
                home_starter = data.get('home_starter', 'TBD')
                print(f"   {matchup}")
                print(f"     Away: {away_starter or 'TBD'}")
                print(f"     Home: {home_starter or 'TBD'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating projected starters: {e}")
        return False

def check_if_update_needed():
    """Check if today's data is already current"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        with open('ProjectedStarters.json', 'r') as f:
            data = json.load(f)
        
        if today in data and len(data[today]) > 0:
            print(f"✅ Today's data ({today}) is already current with {len(data[today])} games")
            return False
        else:
            print(f"⚠️ Today's data ({today}) needs updating")
            return True
            
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ ProjectedStarters.json missing or corrupted, needs updating")
        return True

if __name__ == "__main__":
    print("🎯 PROJECTED STARTERS AUTO-REFRESH")
    print("=" * 40)
    
    if check_if_update_needed():
        success = fetch_and_update_starters()
        if success:
            print("\n🎉 Auto-refresh completed successfully!")
        else:
            print("\n❌ Auto-refresh failed")
    else:
        print("\n🎯 No update needed - data is current")
