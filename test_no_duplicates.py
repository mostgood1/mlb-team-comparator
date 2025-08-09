#!/usr/bin/env python3
import TodaysGames
from datetime import datetime

# Get real games
today = datetime.now().strftime("%Y-%m-%d")
real_games = TodaysGames.get_games_for_date(today)

print(f"Real MLB Games for {today}:")
print("=" * 50)

for i, game in enumerate(real_games, 1):
    print(f"{i:2d}. {game['away_team']} @ {game['home_team']}")

print("\nSample Fallback Games (if API fails):")
print("=" * 50)
sample_games = [
    ('Yankees', 'Red Sox'),
    ('Dodgers', 'Giants'), 
    ('Cubs', 'Cardinals')
]

for i, (away, home) in enumerate(sample_games, 1):
    print(f"{i:2d}. {away} @ {home}")

print(f"\nChecking for conflicts...")
real_matchups = set(f"{g['away_team']} @ {g['home_team']}" for g in real_games)
sample_matchups = set(f"{away} @ {home}" for away, home in sample_games)

conflicts = real_matchups.intersection(sample_matchups)
if conflicts:
    print(f"⚠️ Found {len(conflicts)} conflicts: {conflicts}")
else:
    print("✅ No conflicts between real and sample games!")
