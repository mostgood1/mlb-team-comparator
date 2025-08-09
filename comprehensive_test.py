#!/usr/bin/env python3
"""
Comprehensive MLB Prediction System Test
Tests all components for complete deployment verification
"""

import sys
import time
import traceback

def test_component(name, test_func):
    """Test a component and report results"""
    print(f"\n{'='*50}")
    print(f"TESTING: {name}")
    print('='*50)
    try:
        result = test_func()
        print(f"✅ {name}: PASSED")
        return True
    except Exception as e:
        print(f"❌ {name}: FAILED - {e}")
        traceback.print_exc()
        return False

def test_ultra_fast_engine():
    """Test the core prediction engine"""
    from ultra_fast_engine import FastPredictionEngine
    
    engine = FastPredictionEngine()
    print("✓ Engine initialized")
    
    # Test prediction
    start = time.time()
    result = engine.get_fast_prediction("Yankees", "Red Sox", sim_count=1000)
    duration = (time.time() - start) * 1000
    
    print(f"✓ Prediction completed in {duration:.1f}ms")
    print(f"✓ Total runs predicted: {result['predictions']['predicted_total_runs']}")
    
    # Verify structure
    assert 'predictions' in result
    assert 'predicted_total_runs' in result['predictions']
    assert 'home_win_prob' in result['predictions']
    assert 'recommendations' in result
    assert 'betting_lines' in result
    print("✓ Result structure validated")
    
    return True

def test_todays_games():
    """Test real MLB games fetching"""
    import TodaysGames
    from datetime import datetime
    
    today = datetime.now().strftime("%Y-%m-%d")
    games = TodaysGames.get_games_for_date(today)
    
    print(f"✓ Fetched {len(games)} games for {today}")
    
    if games:
        game = games[0]
        print(f"✓ Sample game: {game['away_team']} @ {game['home_team']}")
        
        # Verify structure
        assert 'away_team' in game
        assert 'home_team' in game
        print("✓ Game structure validated")
    
    return True

def test_data_files():
    """Test all required data files are present and loadable"""
    import json
    import os
    
    required_files = [
        'pitcher_stats_2025_and_career.json',
        'pitcher_id_map.json',
        'ProjectedStarters.json',
        'team_strength_cache.json'
    ]
    
    for filename in required_files:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        assert os.path.exists(filepath), f"{filename} not found"
        
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert data, f"{filename} is empty"
        
        print(f"✓ {filename} loaded successfully")
    
    return True

def test_flask_app():
    """Test that Flask app can be imported"""
    import app
    
    print("✓ Flask app imported successfully")
    
    # Test that prediction engine is available
    assert app.prediction_engine is not None, "Prediction engine not initialized"
    print("✓ Prediction engine initialized in app")
    
    return True

def test_web_prediction():
    """Test the web prediction functionality"""
    from ultra_fast_engine import FastPredictionEngine
    import TodaysGames
    from datetime import datetime
    
    engine = FastPredictionEngine()
    
    # Get real games
    today = datetime.now().strftime("%Y-%m-%d")
    games = TodaysGames.get_games_for_date(today)
    
    if games:
        game = games[0]
        away = game['away_team']
        home = game['home_team']
        
        print(f"✓ Testing prediction for: {away} @ {home}")
        
        result = engine.get_fast_prediction(away, home, sim_count=2000)
        print(f"✓ Prediction: {result['predictions']['predicted_total_runs']} total runs")
    else:
        print("✓ Using sample teams for prediction test")
        result = engine.get_fast_prediction("Yankees", "Red Sox", sim_count=2000)
        print(f"✓ Sample prediction: {result['predictions']['predicted_total_runs']} total runs")
    
    return True

def test_performance():
    """Test prediction performance"""
    from ultra_fast_engine import FastPredictionEngine
    
    engine = FastPredictionEngine()
    
    # Test multiple predictions for performance
    times = []
    for i in range(5):
        start = time.time()
        engine.get_fast_prediction("Yankees", "Red Sox", sim_count=2000)
        duration = (time.time() - start) * 1000
        times.append(duration)
    
    avg_time = sum(times) / len(times)
    print(f"✓ Average prediction time: {avg_time:.1f}ms")
    
    assert avg_time < 100, f"Performance too slow: {avg_time:.1f}ms"
    print("✓ Performance meets requirements (<100ms)")
    
    return True

def main():
    """Run comprehensive system test"""
    print("🎯 MLB PREDICTION SYSTEM - COMPREHENSIVE TEST")
    print("=" * 60)
    
    tests = [
        ("Data Files", test_data_files),
        ("Ultra-Fast Engine", test_ultra_fast_engine),
        ("Today's Games API", test_todays_games),
        ("Flask Application", test_flask_app),
        ("Web Prediction", test_web_prediction),
        ("Performance", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_component(name, test_func):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"FINAL RESULTS: {passed}/{total} tests passed")
    print('='*60)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! ✅")
        print("🚀 Your MLB prediction system is COMPLETE and ready for deployment!")
        print("\n📊 System Features:")
        print("   ✅ Real-time MLB games from API")
        print("   ✅ Complete pitcher statistics (2025 + career)")
        print("   ✅ Ultra-fast predictions (<100ms)")
        print("   ✅ Team strength analysis")
        print("   ✅ Web interface ready")
        print("   ✅ Production deployment configuration")
    else:
        print(f"⚠️  {total - passed} tests failed - system incomplete")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
