#!/usr/bin/env python3
"""
Diagnose win probability calculation issues
"""

import json
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app import app
    
    def test_win_probability_calculations():
        """Test win probability calculations and identify issues"""
        print("🔍 DIAGNOSING WIN PROBABILITY ISSUES")
        print("=" * 45)
        
        with app.test_client() as client:
            response = client.get('/api/fast-predictions')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ API Response: {response.status_code}")
                
                if 'predictions' in data and data['predictions']:
                    print(f"✅ Found {len(data['predictions'])} predictions")
                    
                    print(f"\n📊 WIN PROBABILITY ANALYSIS:")
                    
                    issues_found = []
                    total_games = 0
                    
                    for i, pred in enumerate(data['predictions'][:5]):  # Check first 5 games
                        total_games += 1
                        matchup = f"{pred['away_team']} @ {pred['home_team']}"
                        
                        if 'predictions' in pred:
                            predictions = pred['predictions']
                            
                            # Extract win probabilities
                            home_win_prob = predictions.get('home_win_probability', 'MISSING')
                            away_win_prob = predictions.get('away_win_probability', 'MISSING')
                            
                            print(f"\n🏟️  Game {i+1}: {matchup}")
                            print(f"   📈 Home Win %: {home_win_prob}")
                            print(f"   📈 Away Win %: {away_win_prob}")
                            
                            # Check for issues
                            if home_win_prob == 'MISSING':
                                issues_found.append(f"Game {i+1}: Missing home_win_probability")
                            if away_win_prob == 'MISSING':
                                issues_found.append(f"Game {i+1}: Missing away_win_probability")
                            
                            # Check if probabilities are valid numbers
                            try:
                                home_val = float(home_win_prob) if home_win_prob != 'MISSING' else None
                                away_val = float(away_win_prob) if away_win_prob != 'MISSING' else None
                                
                                if home_val is not None and away_val is not None:
                                    total_prob = home_val + away_val
                                    print(f"   🧮 Total Prob: {total_prob:.4f}")
                                    
                                    # Check if probabilities add up correctly (should be close to 1.0)
                                    if abs(total_prob - 1.0) > 0.01:
                                        issues_found.append(f"Game {i+1}: Probabilities don't sum to 1.0 (sum={total_prob:.4f})")
                                    
                                    # Check if probabilities are in valid range (0-1)
                                    if home_val < 0 or home_val > 1:
                                        issues_found.append(f"Game {i+1}: Home win probability out of range (0-1): {home_val}")
                                    if away_val < 0 or away_val > 1:
                                        issues_found.append(f"Game {i+1}: Away win probability out of range (0-1): {away_val}")
                                    
                                    # Convert to percentages for display
                                    home_pct = home_val * 100
                                    away_pct = away_val * 100
                                    print(f"   📊 Display: Home {home_pct:.1f}% vs Away {away_pct:.1f}%")
                                    
                                else:
                                    issues_found.append(f"Game {i+1}: Could not convert probabilities to numbers")
                                    
                            except ValueError as e:
                                issues_found.append(f"Game {i+1}: Invalid probability format: {e}")
                            
                            # Check other prediction values
                            predicted_home = predictions.get('predicted_home_score', 'MISSING')
                            predicted_away = predictions.get('predicted_away_score', 'MISSING')
                            predicted_total = predictions.get('predicted_total', 'MISSING')
                            confidence = predictions.get('confidence', 'MISSING')
                            
                            print(f"   ⚾ Scores: Away {predicted_away} - Home {predicted_home} (Total: {predicted_total})")
                            print(f"   🎯 Confidence: {confidence}%")
                            
                        else:
                            issues_found.append(f"Game {i+1}: Missing 'predictions' object")
                    
                    print(f"\n🎯 DIAGNOSIS SUMMARY:")
                    if issues_found:
                        print(f"❌ {len(issues_found)} issues found:")
                        for issue in issues_found:
                            print(f"   • {issue}")
                    else:
                        print(f"✅ All {total_games} games have valid win probabilities")
                        
                    # Check cumulative simulation data
                    print(f"\n🔄 CUMULATIVE SYSTEM CHECK:")
                    try:
                        with open('cumulative_simulations.json', 'r') as f:
                            cum_data = json.load(f)
                        
                        print(f"   ✅ Cumulative data loaded: {len(cum_data)} games")
                        
                        # Check first game's cumulative stats
                        if cum_data:
                            first_game_key = list(cum_data.keys())[0]
                            first_game = cum_data[first_game_key]
                            
                            print(f"   📊 Sample game: {first_game_key}")
                            total_sims = first_game.get('total_simulations', 0)
                            home_wins = first_game.get('home_wins', 0)
                            away_wins = first_game.get('away_wins', 0)
                            
                            print(f"   🎲 Total simulations: {total_sims}")
                            print(f"   🏠 Home wins: {home_wins}")
                            print(f"   ✈️  Away wins: {away_wins}")
                            
                            if total_sims > 0:
                                calc_home_prob = home_wins / total_sims
                                calc_away_prob = away_wins / total_sims
                                print(f"   📈 Calculated probabilities: Home {calc_home_prob:.4f}, Away {calc_away_prob:.4f}")
                            else:
                                print(f"   ❌ No simulations recorded!")
                                
                    except Exception as e:
                        print(f"   ❌ Error reading cumulative data: {e}")
                
                else:
                    print("❌ No predictions returned")
            else:
                print(f"❌ API Error: {response.status_code}")

    if __name__ == "__main__":
        test_win_probability_calculations()
        
except Exception as e:
    print(f"❌ Error running test: {e}")
    import traceback
    traceback.print_exc()
