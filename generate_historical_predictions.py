#!/usr/bin/env python3
"""
Generate Predictions for Historical Games
Create predictions for all real games we have actual results for
"""

import json
from datetime import datetime
from ultra_fast_engine import FastPredictionEngine

def _convert_to_short_name(full_name: str) -> str:
    """Convert full team names back to short names"""
    name_mapping = {
        'Los Angeles Angels': 'Angels',
        'Houston Astros': 'Astros', 
        'Oakland Athletics': 'Athletics',
        'Toronto Blue Jays': 'Blue Jays',
        'Cleveland Guardians': 'Guardians',
        'Seattle Mariners': 'Mariners',
        'Baltimore Orioles': 'Orioles',
        'Texas Rangers': 'Rangers',
        'Tampa Bay Rays': 'Rays',
        'Boston Red Sox': 'Red Sox',
        'Kansas City Royals': 'Royals',
        'Detroit Tigers': 'Tigers',
        'Minnesota Twins': 'Twins',
        'Chicago White Sox': 'White Sox',
        'New York Yankees': 'Yankees',
        'Atlanta Braves': 'Braves',
        'Milwaukee Brewers': 'Brewers',
        'St. Louis Cardinals': 'Cardinals',
        'Chicago Cubs': 'Cubs',
        'Arizona Diamondbacks': 'Diamondbacks',
        'Los Angeles Dodgers': 'Dodgers',
        'San Francisco Giants': 'Giants',
        'Miami Marlins': 'Marlins',
        'New York Mets': 'Mets',
        'Washington Nationals': 'Nationals',
        'San Diego Padres': 'Padres',
        'Philadelphia Phillies': 'Phillies',
        'Pittsburgh Pirates': 'Pirates',
        'Cincinnati Reds': 'Reds',
        'Colorado Rockies': 'Rockies'
    }
    return name_mapping.get(full_name, full_name)

def generate_historical_predictions():
    """Generate predictions for all historical games with real results"""
    
    cache_file = "historical_predictions_cache.json"
    
    try:
        # Load current cache
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        engine = FastPredictionEngine()
        total_predictions_added = 0
        
        # Process each date
        for date, date_data in data.items():
            if 'cached_predictions' not in date_data:
                continue
            
            print(f"\\n📅 Processing {date}...")
            
            # Process each game
            for game_key, game_data in date_data['cached_predictions'].items():
                # Only generate predictions for games that have actual results but no predictions
                if (game_data.get('has_real_results', False) and 
                    'actual_away_score' in game_data and 
                    'actual_home_score' in game_data and
                    'predicted_away_score' not in game_data):
                    
                    # Parse team names from game key
                    if ' @ ' in game_key:
                        away_team, home_team = game_key.split(' @ ')
                        
                        # Convert full names to short names for engine
                        away_short = _convert_to_short_name(away_team)
                        home_short = _convert_to_short_name(home_team)
                        
                        print(f"🎯 Generating prediction for {game_key}")
                        print(f"   Teams: {away_team} ({away_short}) @ {home_team} ({home_short})")
                        
                        try:
                            # Generate prediction
                            prediction = engine.get_fast_prediction(away_short, home_short, game_date=date)
                            
                            if prediction and 'predictions' in prediction:
                                pred_away = prediction['predictions']['predicted_away_score']
                                pred_home = prediction['predictions']['predicted_home_score']
                                pred_total = prediction['predictions']['predicted_total_runs']
                                
                                # Add prediction data to game
                                game_data.update({
                                    'predicted_away_score': pred_away,
                                    'predicted_home_score': pred_home,
                                    'predicted_total_runs': pred_total,
                                    'prediction_error_away': abs(pred_away - game_data['actual_away_score']),
                                    'prediction_error_home': abs(pred_home - game_data['actual_home_score']),
                                    'prediction_error_total': abs(pred_total - game_data['actual_total_score']),
                                    'winner_predicted_correctly': _check_winner_prediction(
                                        pred_away, pred_home, 
                                        game_data['actual_away_score'], 
                                        game_data['actual_home_score']
                                    ),
                                    'prediction_generated_timestamp': datetime.now().isoformat()
                                })
                                
                                print(f"   ✅ Predicted: {pred_away:.1f}-{pred_home:.1f} vs Actual: {game_data['actual_away_score']}-{game_data['actual_home_score']}")
                                total_predictions_added += 1
                            else:
                                print(f"   ❌ Could not generate prediction")
                                
                        except Exception as e:
                            print(f"   ❌ Error generating prediction: {e}")
        
        # Save updated data
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\\n✅ Generated {total_predictions_added} new predictions")
        return total_predictions_added
        
    except Exception as e:
        print(f"❌ Error generating predictions: {e}")
        return 0

def _check_winner_prediction(pred_away: float, pred_home: float, actual_away: int, actual_home: int) -> bool:
    """Check if we predicted the winner correctly"""
    predicted_winner = 'home' if pred_home > pred_away else 'away'
    actual_winner = 'home' if actual_home > actual_away else 'away'
    return predicted_winner == actual_winner

if __name__ == "__main__":
    print("🚀 Generating predictions for historical games...")
    count = generate_historical_predictions()
    
    if count > 0:
        print(f"\\n💡 Next steps:")
        print(f"   1. Run: python model_performance_analyzer.py")
        print(f"   2. Review updated analysis with {count} more data points")
        print(f"   3. Apply tuning recommendations if needed")
    else:
        print(f"\\n⚠️ No new predictions generated")
