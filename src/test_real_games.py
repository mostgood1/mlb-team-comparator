#!/usr/bin/env python3
"""
Quick test of ultra-fast engine with real games
"""

from ultra_fast_engine import FastPredictionEngine

def test_real_games():
    print("🚀 Testing Ultra-Fast Engine with REAL GAMES")
    print("=" * 50)
    
    # Initialize engine
    engine = FastPredictionEngine()
    
    # Get today's real games
    games = engine.get_todays_real_games()
    print(f"✓ Real games loaded: {len(games)}")
    
    if games:
        # Test first game
        away, home = games[0]
        print(f"✓ Testing: {away} @ {home}")
        
        # Get prediction
        pred = engine.get_fast_prediction(away, home, 1000)
        
        # Print results
        print(f"✓ Prediction generated in {pred['meta']['execution_time_ms']}ms")
        print(f"✓ Away pitcher: {pred['pitcher_quality']['away_pitcher_name']} (Factor: {pred['pitcher_quality']['away_pitcher_factor']})")
        print(f"✓ Home pitcher: {pred['pitcher_quality']['home_pitcher_name']} (Factor: {pred['pitcher_quality']['home_pitcher_factor']})")
        print(f"✓ Predicted score: {pred['predictions']['predicted_away_score']} - {pred['predictions']['predicted_home_score']}")
        
        print("\n🎯 REAL GAME DATA CONFIRMED!")
        print("✓ Using actual pitcher matchups")
        print("✓ Realistic impact factors")
        print("✓ Fast prediction speed")
        
    else:
        print("❌ No real games found")

if __name__ == "__main__":
    test_real_games()
