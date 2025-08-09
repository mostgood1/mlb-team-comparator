#!/usr/bin/env python3
"""
Simple test to verify historical betting lines are working with real game data
"""

import json
from historical_betting_lines_lookup import HistoricalBettingLinesLookup
from ultra_fast_engine import FastPredictionEngine

def test_with_real_games():
    print("🧪 Testing Historical Betting Lines with Real Games")
    print("=" * 55)
    
    # Check what games we have in current betting lines
    try:
        with open('mlb_betting_lines.json', 'r') as f:
            current_lines = json.load(f)
        
        print("📊 Available games in current betting lines:")
        for date, games in current_lines.items():
            print(f"   {date}: {len(games)} games")
            for game_key in list(games.keys())[:3]:  # Show first 3 games
                away, home = game_key.split('_at_')
                print(f"     - {away} @ {home}")
            if len(games) > 3:
                print(f"     ... and {len(games) - 3} more")
        
        # Test with a real game from current data
        if current_lines:
            latest_date = max(current_lines.keys())
            if current_lines[latest_date]:
                sample_game = list(current_lines[latest_date].keys())[0]
                away_team, home_team = sample_game.split('_at_')
                
                print(f"\n🎯 Testing with real game: {away_team} @ {home_team}")
                print(f"📅 Date: {latest_date}")
                
                # Initialize engine and test
                engine = FastPredictionEngine()
                
                # Test prediction with this real game
                result = engine.get_fast_prediction(away_team, home_team, sim_count=100, game_date=latest_date)
                
                lines = result.get('betting_lines', {})
                print(f"✅ Prediction generated successfully!")
                print(f"   Home ML: {lines.get('home_ml', 'N/A')}")
                print(f"   Away ML: {lines.get('away_ml', 'N/A')}")
                print(f"   Total: {lines.get('total_line', 'N/A')}")
                
                # Test historical lookup specifically
                lookup = HistoricalBettingLinesLookup()
                historical_lines = lookup.get_historical_betting_lines(away_team, home_team, latest_date)
                
                if historical_lines:
                    print(f"✅ Historical lookup successful!")
                    print(f"   Historical ML: {historical_lines.get('moneyline', {})}")
                else:
                    print(f"⚠️ Historical lookup failed")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Show cache stats
    lookup = HistoricalBettingLinesLookup()
    stats = lookup.get_cache_stats()
    print(f"\n📊 CACHE STATISTICS:")
    print(f"   Total cached dates: {stats['total_dates']}")
    print(f"   Total cached games: {stats['total_games']}")
    if stats['total_dates'] > 0:
        print(f"   Date range: {stats['date_range']}")
    
    print(f"\n🎉 Test complete!")

if __name__ == "__main__":
    test_with_real_games()
