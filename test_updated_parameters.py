#!/usr/bin/env python3
"""
Test Updated Model Parameters
Quick test of the updated model on a few sample games
"""

from ultra_fast_engine import FastPredictionEngine
from model_performance_analyzer import ModelPerformanceAnalyzer

def test_updated_parameters():
    """Test the updated model parameters"""
    print("🧪 Testing updated model parameters...")
    print("📊 Current settings: base_runs=4.3, chaos_factor=0.42")
    
    engine = FastPredictionEngine()
    
    # Test a few real games from our historical data
    test_games = [
        ("Astros", "Yankees", "2025-08-09"),
        ("Red Sox", "Padres", "2025-08-08"),
        ("Cubs", "Cardinals", "2025-08-09")
    ]
    
    print(f"\\n🎯 Testing {len(test_games)} sample games...")
    
    for away, home, date in test_games:
        try:
            prediction = engine.get_fast_prediction(away, home, game_date=date)
            
            if prediction and 'predictions' in prediction:
                pred_away = prediction['predictions']['predicted_away_score']
                pred_home = prediction['predictions']['predicted_home_score']
                pred_total = pred_away + pred_home
                
                print(f"\\n🏟️ {away} @ {home}:")
                print(f"   Predicted: {pred_away:.1f}-{pred_home:.1f} (total: {pred_total:.1f})")
                
                # Get actual result if available
                if prediction.get('actual_results'):
                    actual = prediction['actual_results']
                    actual_total = actual['away_score'] + actual['home_score']
                    print(f"   Actual: {actual['away_score']}-{actual['home_score']} (total: {actual_total})")
                    print(f"   Error: {abs(pred_total - actual_total):.1f} runs")
            else:
                print(f"\\n❌ Could not generate prediction for {away} @ {home}")
                
        except Exception as e:
            print(f"\\n❌ Error testing {away} @ {home}: {e}")
    
    print(f"\\n📈 Running full performance analysis...")
    analyzer = ModelPerformanceAnalyzer()
    analysis, recommendations = analyzer.run_full_analysis()
    
    if analysis:
        print(f"\\n🎯 Updated Model Summary:")
        print(f"   • Total games: {analysis['total_games']}")
        print(f"   • Average prediction error: {analysis['total_runs_analysis']['mean_error']:.2f} runs")
        print(f"   • Prediction bias: {analysis['total_runs_analysis']['bias']:+.2f} runs")
        print(f"   • Winner accuracy: {analysis['winner_prediction']['accuracy']:.1%}")
        print(f"   • Predicted avg total: {analysis['scoring_patterns']['avg_predicted_total']:.1f}")
        print(f"   • Actual avg total: {analysis['scoring_patterns']['avg_actual_total']:.1f}")

if __name__ == "__main__":
    test_updated_parameters()
