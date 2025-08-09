#!/usr/bin/env python3
"""
Test the win probability fix
"""

import json
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app import app
    
    def test_win_probability_fix():
        """Test that win probabilities now display correctly"""
        print("🧪 TESTING WIN PROBABILITY FIX")
        print("=" * 35)
        
        with app.test_client() as client:
            response = client.get('/api/fast-predictions')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ API Response: {response.status_code}")
                
                if 'predictions' in data and data['predictions']:
                    print(f"✅ Found {len(data['predictions'])} predictions")
                    
                    # Test first prediction
                    first_pred = data['predictions'][0]
                    matchup = f"{first_pred['away_team']} @ {first_pred['home_team']}"
                    
                    print(f"\n🏟️  Testing: {matchup}")
                    
                    if 'predictions' in first_pred:
                        pred = first_pred['predictions']
                        
                        home_win_prob = pred.get('home_win_probability', 'MISSING')
                        away_win_prob = pred.get('away_win_probability', 'MISSING')
                        
                        print(f"📊 Raw API Data:")
                        print(f"   home_win_probability: {home_win_prob}")
                        print(f"   away_win_probability: {away_win_prob}")
                        
                        if home_win_prob != 'MISSING' and away_win_prob != 'MISSING':
                            # Test the JavaScript display logic
                            home_pct = home_win_prob * 100
                            away_pct = away_win_prob * 100
                            
                            print(f"\n🎯 Display Format:")
                            print(f"   🏠 Home: {home_pct:.1f}%")
                            print(f"   ✈️  Away: {away_pct:.1f}%")
                            print(f"   📈 Total: {(home_pct + away_pct):.1f}%")
                            
                            # Check for precision issues
                            if abs((home_win_prob + away_win_prob) - 1.0) < 0.001:
                                print(f"   ✅ Probabilities sum correctly")
                            else:
                                print(f"   ⚠️  Probabilities don't sum to 1.0")
                            
                            # Check for excessive precision
                            home_str = str(home_win_prob)
                            away_str = str(away_win_prob)
                            
                            if len(home_str.split('.')[-1]) <= 4 and len(away_str.split('.')[-1]) <= 4:
                                print(f"   ✅ Precision is reasonable")
                            else:
                                print(f"   ⚠️  Excessive decimal precision")
                        
                        print(f"\n💡 EXPECTED WEB DISPLAY:")
                        if home_win_prob != 'MISSING' and away_win_prob != 'MISSING':
                            display_text = f"🏠 {(home_win_prob * 100):.1f}% | ✈️ {(away_win_prob * 100):.1f}%"
                            print(f"   {display_text}")
                        else:
                            print(f"   ❌ Cannot display - missing data")
                    
                    else:
                        print(f"❌ Missing predictions object")
                
                else:
                    print("❌ No predictions returned")
            else:
                print(f"❌ API Error: {response.status_code}")

    if __name__ == "__main__":
        test_win_probability_fix()
        
except Exception as e:
    print(f"❌ Error running test: {e}")
    import traceback
    traceback.print_exc()
