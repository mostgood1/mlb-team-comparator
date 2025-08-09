#!/usr/bin/env python3
from ultra_fast_engine import FastPredictionEngine
import json
import os

print("🎯 TESTING AUTO-REFRESH FUNCTIONALITY")
print("=" * 50)

# Let's temporarily remove today's data to test auto-refresh
print("1. Checking current data...")
with open('ProjectedStarters.json', 'r') as f:
    data = json.load(f)

from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')

# Backup today's data
today_backup = data.get(today, {})
print(f"   Today ({today}): {len(today_backup)} games")

# Remove today's data to test auto-refresh
if today in data:
    del data[today]
    with open('ProjectedStarters.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("2. ✅ Temporarily removed today's data")

# Now initialize the engine - should trigger auto-refresh
print("3. 🔄 Initializing engine (should auto-refresh)...")
engine = FastPredictionEngine()

# Check if data was restored
print("4. 📊 Checking if auto-refresh worked...")
with open('ProjectedStarters.json', 'r') as f:
    updated_data = json.load(f)

if today in updated_data:
    games_count = len(updated_data[today])
    print(f"   ✅ Auto-refresh SUCCESS! Found {games_count} games for today")
    
    # Show sample
    sample_games = list(updated_data[today].items())[:2]
    for matchup, details in sample_games:
        print(f"      {matchup}")
        print(f"        Away: {details.get('away_starter', 'TBD')}")
        print(f"        Home: {details.get('home_starter', 'TBD')}")
else:
    print("   ❌ Auto-refresh failed")

print("\n🎯 Auto-refresh test completed!")
