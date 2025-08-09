#!/usr/bin/env python3
"""
Test Historical Betting Lines Integration
Tests the complete historical betting lines system with the ultra-fast engine
"""

from ultra_fast_engine import FastPredictionEngine
from historical_betting_lines_lookup import HistoricalBettingLinesLookup
from datetime import datetime, timedelta

def test_historical_betting_integration():
    print("🧪 Testing Historical Betting Lines Integration")
    print("=" * 60)
    
    # Initialize components
    engine = FastPredictionEngine()
    historical_lookup = HistoricalBettingLinesLookup()
    
    # Test dates
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    print(f"📅 Today: {today}")
    print(f"📅 Yesterday: {yesterday}")
    print(f"📅 Week ago: {week_ago}")
    
    # Test games
    test_games = [
        ("Yankees", "Rangers"),
        ("Dodgers", "Athletics"),
        ("Cincinnati Reds", "Pittsburgh Pirates")
    ]
    
    for away, home in test_games:
        print(f"\n🎯 Testing: {away} @ {home}")
        print("-" * 50)
        
        # Test current day (should use real lines if available)
        print(f"📈 CURRENT DAY ({today}):")
        try:
            result_today = engine.get_fast_prediction(away, home, sim_count=100, game_date=today)
            lines_today = result_today.get('betting_lines', {})
            print(f"   Home ML: {lines_today.get('home_ml', 'N/A')}")
            print(f"   Away ML: {lines_today.get('away_ml', 'N/A')}")
            print(f"   Total: {lines_today.get('total_line', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test yesterday (should use historical lines)
        print(f"📊 YESTERDAY ({yesterday}):")
        try:
            result_yesterday = engine.get_fast_prediction(away, home, sim_count=100, game_date=yesterday)
            lines_yesterday = result_yesterday.get('betting_lines', {})
            print(f"   Home ML: {lines_yesterday.get('home_ml', 'N/A')}")
            print(f"   Away ML: {lines_yesterday.get('away_ml', 'N/A')}")
            print(f"   Total: {lines_yesterday.get('total_line', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test week ago (should use historical lines)
        print(f"🔍 WEEK AGO ({week_ago}):")
        try:
            result_week_ago = engine.get_fast_prediction(away, home, sim_count=100, game_date=week_ago)
            lines_week_ago = result_week_ago.get('betting_lines', {})
            print(f"   Home ML: {lines_week_ago.get('home_ml', 'N/A')}")
            print(f"   Away ML: {lines_week_ago.get('away_ml', 'N/A')}")
            print(f"   Total: {lines_week_ago.get('total_line', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Show cache statistics
    print(f"\n📊 CACHE STATISTICS:")
    stats = historical_lookup.get_cache_stats()
    print(f"   Total cached dates: {stats['total_dates']}")
    print(f"   Total cached games: {stats['total_games']}")
    print(f"   Date range: {stats['date_range']}")
    if stats['cache_file_size_mb'] > 0:
        print(f"   Cache file size: {stats['cache_file_size_mb']:.2f} MB")
    
    print(f"\n🎉 Historical betting lines integration test complete!")

def test_specific_historical_date():
    """Test historical betting lines for a specific past date"""
    print("\n🔍 Testing Specific Historical Date")
    print("=" * 40)
    
    lookup = HistoricalBettingLinesLookup()
    test_date = "2025-08-06"  # Two days ago
    
    print(f"📅 Fetching historical betting lines for {test_date}")
    
    # Fetch lines for the entire date
    success = lookup.fetch_historical_lines_for_date(test_date)
    if success:
        print(f"✅ Successfully cached betting lines for {test_date}")
        
        # Test specific game lookup
        lines = lookup.get_historical_betting_lines("Yankees", "Rangers", test_date)
        if lines:
            print(f"🎯 Sample historical lines for Yankees @ Rangers:")
            print(f"   Moneyline: {lines.get('moneyline', {})}")
            if lines.get('total'):
                total_info = lines['total'][0] if isinstance(lines['total'], list) else lines['total']
                print(f"   Total: {total_info.get('point', 'N/A')} ({total_info.get('price', 'N/A')})")
        else:
            print("⚠️ No lines found for specific game")
    else:
        print(f"❌ Failed to fetch betting lines for {test_date}")

if __name__ == "__main__":
    test_historical_betting_integration()
    test_specific_historical_date()
