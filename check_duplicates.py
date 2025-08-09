#!/usr/bin/env python3
import TodaysGames
from datetime import datetime
import json

# Test for today's date
today = datetime.now().strftime("%Y-%m-%d")
print(f"Checking games for {today}...")

games = TodaysGames.get_games_for_date(today)
print(f"Raw API returned {len(games)} games")

print("\n" + "="*60)
print("ALL GAMES FROM API:")
print("="*60)

seen_games = set()
duplicates = []

for i, game in enumerate(games):
    game_key = f"{game['away_team']} @ {game['home_team']}"
    
    if game_key in seen_games:
        duplicates.append((i, game_key, game))
        print(f"{i+1:2d}. {game_key} - ⚠️ DUPLICATE")
    else:
        seen_games.add(game_key)
        print(f"{i+1:2d}. {game_key} - {game.get('status', 'Unknown')} - Game PK: {game.get('game_pk', 'N/A')}")

if duplicates:
    print(f"\n⚠️ Found {len(duplicates)} duplicate games:")
    for idx, game_key, game in duplicates:
        print(f"   Index {idx}: {game_key}")
        print(f"   Game PK: {game.get('game_pk', 'N/A')}")
        print(f"   Status: {game.get('status', 'Unknown')}")
        print(f"   Time: {game.get('game_time', 'N/A')}")
        print()
else:
    print("\n✅ No duplicates found!")

print(f"\nUnique games: {len(seen_games)}")
print(f"Total games from API: {len(games)}")
