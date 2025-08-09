#!/usr/bin/env python3
"""
Test the ultra-fast engine with real betting lines integration
"""

from ultra_fast_engine import FastPredictionEngine
from datetime import datetime

def test_real_betting_lines():
    print("🧪 Testing Ultra-Fast Engine with Real Betting Lines")
    print("=" * 60)
    
    engine = FastPredictionEngine()
    
    # Test with today's games
    test_games = [
        ("Cincinnati Reds", "Pittsburgh Pirates"),
        ("Yankees", "Rangers"),  
        ("Dodgers", "Athletics")
    ]
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for away, home in test_games:
        print(f"\n🎯 Testing: {away} @ {home}")
        print("-" * 40)
        
        try:
            # Get prediction with real betting lines
            result = engine.get_fast_prediction(away, home, sim_count=100, game_date=today)
            
            # Show betting lines info
            lines = result.get('betting_lines', {})
            print(f"🏠 Home ML: {lines.get('home_ml', 'N/A')}")
            print(f"✈️  Away ML: {lines.get('away_ml', 'N/A')}")
            print(f"📊 Total: {lines.get('total_line', 'N/A')}")
            
            # Show predictions
            print(f"🔮 Home Win Prob: {result.get('home_win_prob', 0):.1%}")
            print(f"🔮 Predicted Total: {result.get('predicted_total', 0):.1f}")
            
            # Show betting recommendations
            recommendations = result.get('betting_recommendations', [])
            if recommendations:
                print(f"💰 Betting Recs: {len(recommendations)} found")
                for rec in recommendations[:2]:  # Show first 2
                    print(f"   {rec.get('type', 'Unknown')}: {rec.get('description', 'N/A')}")
            else:
                print("💰 No betting value identified")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Real betting lines integration test complete!")

if __name__ == "__main__":
    test_real_betting_lines()
