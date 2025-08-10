#!/usr/bin/env python3
"""
Model Performance Analysis and Retuning
Analyze predictions vs actual results to improve simulation accuracy
"""

import json
import os
from typing import Dict, List, Tuple
import statistics
import numpy as np

class ModelPerformanceAnalyzer:
    """Analyze prediction accuracy and suggest model improvements"""
    
    def __init__(self):
        self.cache_file = "historical_predictions_cache.json"
        self.analysis_results = {}
        
    def load_historical_data(self) -> Dict:
        """Load historical predictions and results"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading historical data: {e}")
            return {}
    
    def analyze_prediction_accuracy(self, historical_data: Dict) -> Dict:
        """Comprehensive analysis of prediction accuracy"""
        analysis = {
            'total_games': 0,
            'dates_analyzed': [],
            'total_runs_analysis': {
                'predicted': [],
                'actual': [],
                'errors': [],
                'mean_error': 0,
                'rmse': 0,
                'bias': 0
            },
            'individual_scores_analysis': {
                'away_predicted': [],
                'away_actual': [],
                'home_predicted': [],
                'home_actual': [],
                'away_errors': [],
                'home_errors': []
            },
            'winner_prediction': {
                'correct': 0,
                'total': 0,
                'accuracy': 0
            },
            'scoring_patterns': {
                'avg_predicted_total': 0,
                'avg_actual_total': 0,
                'prediction_bias': 0
            },
            'game_details': []
        }
        
        all_games = []
        
        # Collect data from all dates
        for date, date_data in historical_data.items():
            if 'cached_predictions' in date_data:
                analysis['dates_analyzed'].append(date)
                predictions = date_data['cached_predictions']
                
                for game_key, game_data in predictions.items():
                    if all(key in game_data for key in ['predicted_away_score', 'predicted_home_score', 'actual_away_score', 'actual_home_score']):
                        game_analysis = self._analyze_single_game(game_key, game_data)
                        all_games.append(game_analysis)
                        analysis['game_details'].append(game_analysis)
        
        analysis['total_games'] = len(all_games)
        
        if all_games:
            # Total runs analysis
            predicted_totals = [g['predicted_total'] for g in all_games]
            actual_totals = [g['actual_total'] for g in all_games]
            total_errors = [abs(p - a) for p, a in zip(predicted_totals, actual_totals)]
            
            analysis['total_runs_analysis'] = {
                'predicted': predicted_totals,
                'actual': actual_totals,
                'errors': total_errors,
                'mean_error': statistics.mean(total_errors),
                'rmse': np.sqrt(np.mean([(p - a) ** 2 for p, a in zip(predicted_totals, actual_totals)])),
                'bias': statistics.mean([p - a for p, a in zip(predicted_totals, actual_totals)])
            }
            
            # Individual scores analysis
            away_predicted = [g['predicted_away'] for g in all_games]
            away_actual = [g['actual_away'] for g in all_games]
            home_predicted = [g['predicted_home'] for g in all_games]
            home_actual = [g['actual_home'] for g in all_games]
            
            analysis['individual_scores_analysis'] = {
                'away_predicted': away_predicted,
                'away_actual': away_actual,
                'home_predicted': home_predicted,
                'home_actual': home_actual,
                'away_errors': [abs(p - a) for p, a in zip(away_predicted, away_actual)],
                'home_errors': [abs(p - a) for p, a in zip(home_predicted, home_actual)],
                'away_bias': statistics.mean([p - a for p, a in zip(away_predicted, away_actual)]),
                'home_bias': statistics.mean([p - a for p, a in zip(home_predicted, home_actual)])
            }
            
            # Winner prediction analysis
            winners_correct = sum(1 for g in all_games if g['winner_correct'])
            analysis['winner_prediction'] = {
                'correct': winners_correct,
                'total': len(all_games),
                'accuracy': winners_correct / len(all_games) if all_games else 0
            }
            
            # Scoring patterns
            analysis['scoring_patterns'] = {
                'avg_predicted_total': statistics.mean(predicted_totals),
                'avg_actual_total': statistics.mean(actual_totals),
                'prediction_bias': statistics.mean([p - a for p, a in zip(predicted_totals, actual_totals)])
            }
        
        return analysis
    
    def _analyze_single_game(self, game_key: str, game_data: Dict) -> Dict:
        """Analyze a single game's prediction accuracy"""
        predicted_away = game_data['predicted_away_score']
        predicted_home = game_data['predicted_home_score']
        actual_away = game_data['actual_away_score']
        actual_home = game_data['actual_home_score']
        
        predicted_total = predicted_away + predicted_home
        actual_total = actual_away + actual_home
        
        # Winner prediction
        predicted_winner = 'home' if predicted_home > predicted_away else 'away'
        actual_winner = 'home' if actual_home > actual_away else 'away'
        winner_correct = predicted_winner == actual_winner
        
        return {
            'game': game_key,
            'predicted_away': predicted_away,
            'predicted_home': predicted_home,
            'actual_away': actual_away,
            'actual_home': actual_home,
            'predicted_total': predicted_total,
            'actual_total': actual_total,
            'total_error': abs(predicted_total - actual_total),
            'away_error': abs(predicted_away - actual_away),
            'home_error': abs(predicted_home - actual_home),
            'winner_correct': winner_correct,
            'predicted_winner': predicted_winner,
            'actual_winner': actual_winner
        }
    
    def generate_tuning_recommendations(self, analysis: Dict) -> Dict:
        """Generate specific recommendations for model tuning"""
        recommendations = {
            'base_scoring_adjustment': {},
            'variance_adjustment': {},
            'home_field_advantage': {},
            'pitcher_impact': {},
            'summary': []
        }
        
        if analysis['total_games'] == 0:
            return recommendations
        
        # Base scoring analysis
        predicted_avg = analysis['scoring_patterns']['avg_predicted_total']
        actual_avg = analysis['scoring_patterns']['avg_actual_total']
        bias = analysis['total_runs_analysis']['bias']
        
        # Current base_runs_per_team is 3.75, so total expected is 7.5
        current_base = 3.75
        target_total = actual_avg
        suggested_base = (target_total / 2)  # Divide by 2 since we have away + home
        
        recommendations['base_scoring_adjustment'] = {
            'current_base_runs_per_team': current_base,
            'suggested_base_runs_per_team': round(suggested_base, 2),
            'adjustment_needed': round(suggested_base - current_base, 2),
            'reasoning': f"Predicted avg: {predicted_avg:.1f}, Actual avg: {actual_avg:.1f}, Bias: {bias:.1f}"
        }
        
        # Variance analysis
        actual_std = np.std(analysis['total_runs_analysis']['actual'])
        predicted_std = np.std(analysis['total_runs_analysis']['predicted'])
        
        # Current game_chaos_factor std is 0.20
        current_chaos = 0.20
        variance_ratio = actual_std / predicted_std if predicted_std > 0 else 1.0
        suggested_chaos = min(0.35, max(0.10, current_chaos * variance_ratio))
        
        recommendations['variance_adjustment'] = {
            'current_chaos_factor_std': current_chaos,
            'suggested_chaos_factor_std': round(suggested_chaos, 3),
            'actual_std_dev': round(actual_std, 2),
            'predicted_std_dev': round(predicted_std, 2),
            'variance_ratio': round(variance_ratio, 2)
        }
        
        # Home field advantage analysis
        home_bias = analysis['individual_scores_analysis']['home_bias']
        away_bias = analysis['individual_scores_analysis']['away_bias']
        
        # Current home field advantage is 0.15
        current_hfa = 0.15
        home_advantage_effectiveness = home_bias - away_bias
        
        recommendations['home_field_advantage'] = {
            'current_hfa': current_hfa,
            'home_bias': round(home_bias, 2),
            'away_bias': round(away_bias, 2),
            'net_home_advantage': round(home_advantage_effectiveness, 2),
            'suggested_adjustment': 'maintain' if abs(home_advantage_effectiveness) < 0.3 else 'adjust'
        }
        
        # Winner prediction analysis
        winner_accuracy = analysis['winner_prediction']['accuracy']
        recommendations['winner_accuracy'] = {
            'current_accuracy': round(winner_accuracy * 100, 1),
            'target_accuracy': '52-58%',
            'status': 'good' if 0.52 <= winner_accuracy <= 0.58 else 'needs_improvement'
        }
        
        # Generate summary recommendations
        summary = []
        
        if abs(bias) > 0.5:
            summary.append(f"🎯 CRITICAL: Adjust base scoring from {current_base} to {suggested_base:.2f} (bias: {bias:+.1f} runs)")
        
        if variance_ratio > 1.2 or variance_ratio < 0.8:
            summary.append(f"📊 Adjust variance: chaos factor from {current_chaos} to {suggested_chaos:.3f} (ratio: {variance_ratio:.2f})")
        
        if winner_accuracy < 0.50:
            summary.append(f"⚠️ Winner prediction accuracy low: {winner_accuracy:.1%} (target: 52-58%)")
        elif winner_accuracy > 0.60:
            summary.append(f"🎲 Winner prediction too high: {winner_accuracy:.1%} (may indicate overfitting)")
        
        recommendations['summary'] = summary
        
        return recommendations
    
    def print_analysis_report(self, analysis: Dict, recommendations: Dict):
        """Print comprehensive analysis report"""
        print("=" * 80)
        print("🔬 MODEL PERFORMANCE ANALYSIS & TUNING RECOMMENDATIONS")
        print("=" * 80)
        
        print(f"\n📊 DATASET OVERVIEW:")
        print(f"   • Total games analyzed: {analysis['total_games']}")
        print(f"   • Dates: {', '.join(analysis['dates_analyzed'])}")
        
        if analysis['total_games'] == 0:
            print("❌ No data available for analysis")
            return
        
        print(f"\n🎯 TOTAL RUNS ACCURACY:")
        total_analysis = analysis['total_runs_analysis']
        print(f"   • Mean prediction error: {total_analysis['mean_error']:.2f} runs")
        print(f"   • RMSE: {total_analysis['rmse']:.2f}")
        print(f"   • Prediction bias: {total_analysis['bias']:+.2f} runs")
        print(f"   • Predicted avg: {analysis['scoring_patterns']['avg_predicted_total']:.1f}")
        print(f"   • Actual avg: {analysis['scoring_patterns']['avg_actual_total']:.1f}")
        
        print(f"\n🏆 WINNER PREDICTION:")
        winner = analysis['winner_prediction']
        print(f"   • Accuracy: {winner['accuracy']:.1%} ({winner['correct']}/{winner['total']})")
        print(f"   • Target range: 52-58% (sports betting baseline)")
        
        print(f"\n🏠 INDIVIDUAL SCORES:")
        individual = analysis['individual_scores_analysis']
        print(f"   • Away team bias: {individual['away_bias']:+.2f} runs")
        print(f"   • Home team bias: {individual['home_bias']:+.2f} runs")
        print(f"   • Average away error: {statistics.mean(individual['away_errors']):.2f}")
        print(f"   • Average home error: {statistics.mean(individual['home_errors']):.2f}")
        
        print(f"\n🔧 TUNING RECOMMENDATIONS:")
        if recommendations['summary']:
            for rec in recommendations['summary']:
                print(f"   {rec}")
        else:
            print("   ✅ Model parameters appear well-calibrated")
        
        print(f"\n📈 DETAILED PARAMETER SUGGESTIONS:")
        base_adj = recommendations['base_scoring_adjustment']
        print(f"   • Base runs per team: {base_adj['current_base_runs_per_team']} → {base_adj['suggested_base_runs_per_team']}")
        
        var_adj = recommendations['variance_adjustment']
        print(f"   • Chaos factor std: {var_adj['current_chaos_factor_std']} → {var_adj['suggested_chaos_factor_std']}")
        
        print(f"\n🎲 VARIANCE ANALYSIS:")
        print(f"   • Actual std dev: {var_adj['actual_std_dev']} runs")
        print(f"   • Predicted std dev: {var_adj['predicted_std_dev']} runs")
        print(f"   • Variance ratio: {var_adj['variance_ratio']:.2f}")
        
    def run_full_analysis(self):
        """Run complete analysis and generate recommendations"""
        print("🔍 Loading historical data...")
        historical_data = self.load_historical_data()
        
        if not historical_data:
            print("❌ No historical data available")
            return None, None
        
        print("📊 Analyzing prediction accuracy...")
        analysis = self.analyze_prediction_accuracy(historical_data)
        
        print("🔧 Generating tuning recommendations...")
        recommendations = self.generate_tuning_recommendations(analysis)
        
        self.print_analysis_report(analysis, recommendations)
        
        return analysis, recommendations

def main():
    """Run the model performance analysis"""
    analyzer = ModelPerformanceAnalyzer()
    analysis, recommendations = analyzer.run_full_analysis()
    
    if recommendations and recommendations['summary']:
        print(f"\n💡 IMPLEMENTATION PRIORITY:")
        print(f"   1. Apply base scoring adjustment first")
        print(f"   2. Test with new parameters on historical data")
        print(f"   3. Adjust variance if needed")
        print(f"   4. Monitor winner prediction accuracy")

if __name__ == "__main__":
    main()
