"""
Ultra-Fast MLB Prediction Web Interface
Real-time betting recommendations with sub-200ms prediction generation
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import traceback
from datetime import datetime
from typing import Dict, List

# Import the ultra-fast engine
try:
    from ultra_fast_engine import FastPredictionEngine
    print("✓ Ultra-fast engine imported successfully")
    ULTRA_FAST_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Ultra-fast engine not available: {e}")
    ULTRA_FAST_AVAILABLE = False

# Fallback imports - skip if not available
IMPROVED_AVAILABLE = False
try:
    from improved_prediction_engine import ImprovedMLBPredictionEngine
    print("✓ Improved engine available as fallback")
    IMPROVED_AVAILABLE = True
except ImportError:
    print("ℹ Improved engine not available (using ultra-fast only)")

# Configure Flask to serve static files from current directory
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# Initialize prediction engine
prediction_engine = None
if ULTRA_FAST_AVAILABLE:
    try:
        prediction_engine = FastPredictionEngine()
        print("✓ Ultra-fast prediction engine initialized")
    except Exception as e:
        print(f"❌ Failed to initialize prediction engine: {e}")
else:
    print("❌ No prediction engine available")

@app.route('/')
def home():
    """Main page with ultra-fast prediction interface using real games"""
    return render_template('index.html')

@app.route('/api/real-games-predictions')
def get_real_games_predictions():
    """Get predictions for today's real games with actual pitcher matchups"""
    try:
        if ULTRA_FAST_AVAILABLE:
            engine = FastPredictionEngine()
            
            # Get date parameter (default to today)
            game_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            # Get today's real games
            real_games = engine.get_todays_real_games(game_date)
            
            if not real_games:
                return jsonify({
                    'success': True,
                    'predictions': [],
                    'message': f'No games found for {game_date}',
                    'date': game_date
                })
            
            # Generate predictions for all real games
            predictions = []
            for away_team, home_team in real_games:
                try:
                    prediction = engine.get_fast_prediction(away_team, home_team, sim_count=2000, game_date=game_date)
                    predictions.append(prediction)
                except Exception as e:
                    print(f"Error predicting {away_team} @ {home_team}: {e}")
                    continue
            
            return jsonify({
                'success': True,
                'predictions': predictions,
                'total_games': len(predictions),
                'date': game_date,
                'version': 'OPTIMIZED v2.2'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Prediction engine not available',
                'predictions': []
            })
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'predictions': []
        })

@app.route('/api/check-historical-data')
def check_historical_data():
    """Check what historical data is available"""
    try:
        cache_file = 'historical_predictions_cache.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                historical_data = json.load(f)
            
            available_dates = list(historical_data.keys())
            game_counts = {}
            
            for date, data in historical_data.items():
                cached_predictions = data.get('cached_predictions', {})
                game_counts[date] = len(cached_predictions)
            
            return jsonify({
                'success': True,
                'available_dates': sorted(available_dates),
                'game_counts': game_counts,
                'total_dates': len(available_dates)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Historical cache file not found',
                'available_dates': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'available_dates': []
        })

@app.route('/api/games-predictions')
def get_games_predictions():
    """Get predictions for multiple games - supports both current and historical"""
    try:
        game_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if ULTRA_FAST_AVAILABLE:
            engine = FastPredictionEngine()
            
            # Get real games for the date
            real_games = engine.get_todays_real_games(game_date)
            
            predictions = []
            for away_team, home_team in real_games[:10]:  # Limit to 10 games for performance
                try:
                    prediction = engine.get_fast_prediction(away_team, home_team, sim_count=1000, game_date=game_date)
                    predictions.append(prediction)
                except Exception as e:
                    print(f"Error predicting {away_team} @ {home_team}: {e}")
                    continue
            
            return jsonify({
                'success': True,
                'predictions': predictions,
                'total_games': len(predictions),
                'date': game_date
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Prediction engine not available'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/speed-test')
def speed_test():
    """Test prediction speed with a sample game"""
    try:
        if ULTRA_FAST_AVAILABLE:
            engine = FastPredictionEngine()
            
            # Use a sample matchup for speed testing
            start_time = datetime.now()
            prediction = engine.get_fast_prediction("Yankees", "Dodgers", sim_count=1000)
            end_time = datetime.now()
            
            execution_time = (end_time - start_time).total_seconds() * 1000
            
            return jsonify({
                'success': True,
                'execution_time_ms': round(execution_time, 2),
                'predictions': prediction,
                'test_matchup': 'Yankees @ Dodgers',
                'sim_count': 1000
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Prediction engine not available'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/version')
def get_version():
    """Get current model version and parameters"""
    try:
        if ULTRA_FAST_AVAILABLE:
            return jsonify({
                'success': True,
                'version': 'OPTIMIZED v2.2',
                'model_parameters': {
                    'base_runs_per_team': 4.3,
                    'chaos_factor_std': 0.42,
                    'chaos_bounds': [0.75, 1.25],
                    'team_multiplier_bounds': [0.6, 1.4]
                },
                'features': [
                    'Realistic MLB scoring (8-9 run average)',
                    'Pitcher quality integration',
                    'Sub-20ms predictions',
                    'Historical betting analysis'
                ],
                'last_updated': '2025-08-10'
            })
        else:
            return jsonify({
                'success': False,
                'version': 'ENGINE_NOT_AVAILABLE',
                'error': 'Prediction engine not loaded'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/status')
def get_status():
    """Get system status and health check"""
    try:
        status = {
            'ultra_fast_engine': ULTRA_FAST_AVAILABLE,
            'improved_engine': IMPROVED_AVAILABLE,
            'prediction_engine_loaded': prediction_engine is not None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Test a quick prediction if engine is available
        if ULTRA_FAST_AVAILABLE and prediction_engine:
            try:
                test_start = datetime.now()
                test_prediction = prediction_engine.get_fast_prediction("Yankees", "Dodgers", sim_count=100)
                test_time = (datetime.now() - test_start).total_seconds() * 1000
                status['prediction_test'] = {
                    'success': True,
                    'execution_time_ms': round(test_time, 2)
                }
            except Exception as e:
                status['prediction_test'] = {
                    'success': False,
                    'error': str(e)
                }
        
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🚀 Starting Ultra-Fast MLB Prediction Server...")
    print(f"✓ Ultra-fast engine: {'Available' if ULTRA_FAST_AVAILABLE else 'Not Available'}")
    print(f"✓ Improved engine: {'Available' if IMPROVED_AVAILABLE else 'Not Available'}")
    
    # Use PORT environment variable for Render deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
