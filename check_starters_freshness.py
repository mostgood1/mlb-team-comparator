#!/usr/bin/env python3
import json
from datetime import datetime

print("CHECKING PROJECTED STARTERS DATA")
print("=" * 50)

# Check what dates are in the ProjectedStarters.json
with open('ProjectedStarters.json', 'r') as f:
    starters_data = json.load(f)

print(f"Dates available in ProjectedStarters.json:")
for date in sorted(starters_data.keys()):
    matchups = len(starters_data[date])
    print(f"  {date}: {matchups} matchups")

today = datetime.now().strftime('%Y-%m-%d')
print(f"\nToday is: {today}")

if today in starters_data:
    print(f"✅ Today's pitching matchups are available!")
    print(f"   Found {len(starters_data[today])} games for today")
    
    # Show sample matchups
    print("\nSample today's matchups:")
    for i, (matchup, data) in enumerate(list(starters_data[today].items())[:3]):
        away_starter = data.get('away_starter', 'TBD')
        home_starter = data.get('home_starter', 'TBD')
        print(f"  {matchup}")
        print(f"    Away: {away_starter}")
        print(f"    Home: {home_starter}")
else:
    print(f"⚠️  Today's pitching matchups are NOT available")
    print("   The ProjectedStarters.json needs to be updated")
    
    # Check most recent date
    if starters_data:
        latest_date = max(starters_data.keys())
        print(f"   Most recent data: {latest_date}")
    else:
        print("   File is empty")

print(f"\nTotal dates in file: {len(starters_data)}")
print(f"Total unique matchups across all dates: {sum(len(games) for games in starters_data.values())}")
