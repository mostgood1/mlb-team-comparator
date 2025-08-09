#!/usr/bin/env python3
import TodaysGames
import datetime

# Test for today's date
today = datetime.datetime.now().strftime("%Y-%m-%d")
print(f"Testing TodaysGames for {today}...")

games = TodaysGames.get_games_for_date(today)
print(f"Found {len(games)} games for today:")

for game in games[:5]:  # Show first 5 games
    print(f"  {game['away_team']} @ {game['home_team']} ({game['status']})")

print("\n✅ TodaysGames module is working!")
