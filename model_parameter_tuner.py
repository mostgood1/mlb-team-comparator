#!/usr/bin/env python3
"""
Model Parameter Tuner
Apply recommendations from performance analysis to improve prediction accuracy
"""

import json
import shutil
from datetime import datetime
from typing import Dict, List
import re

class ModelParameterTuner:
    """Apply tuning recommendations to model parameters"""
    
    def __init__(self):
        self.engine_file = "ultra_fast_engine.py"
        self.backup_file = f"ultra_fast_engine_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        
    def create_backup(self):
        """Create backup of current engine file"""
        try:
            shutil.copy2(self.engine_file, self.backup_file)
            print(f"✅ Created backup: {self.backup_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def read_engine_file(self) -> str:
        """Read the current engine file"""
        try:
            with open(self.engine_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading engine file: {e}")
            return ""
    
    def write_engine_file(self, content: str) -> bool:
        """Write updated content to engine file"""
        try:
            with open(self.engine_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated {self.engine_file}")
            return True
        except Exception as e:
            print(f"❌ Error writing engine file: {e}")
            return False
    
    def apply_base_scoring_adjustment(self, content: str, new_base: float) -> str:
        """Adjust base_runs_per_team parameter"""
        # Pattern to find base_runs_per_team assignment
        pattern = r'(base_runs_per_team\s*=\s*)([0-9]*\.?[0-9]+)'
        
        def replacement(match):
            return f"{match.group(1)}{new_base}"
        
        new_content = re.sub(pattern, replacement, content)
        
        # Also check for any hardcoded 3.75 values in simulation logic
        pattern2 = r'(\b3\.75\b)'
        new_content = re.sub(pattern2, str(new_base), new_content)
        
        print(f"🎯 Applied base scoring adjustment: 3.75 → {new_base}")
        return new_content
    
    def apply_variance_adjustment(self, content: str, new_chaos: float) -> str:
        """Adjust game_chaos_factor std parameter"""
        # Pattern to find chaos factor in normal distribution
        pattern = r'(np\.random\.normal\([^,]+,\s*)([0-9]*\.?[0-9]+)(\s*,\s*sim_count\))'
        
        def replacement(match):
            return f"{match.group(1)}{new_chaos}{match.group(3)}"
        
        new_content = re.sub(pattern, replacement, content)
        
        # Also look for explicit chaos_factor variable
        pattern2 = r'(chaos_factor\s*=\s*)([0-9]*\.?[0-9]+)'
        new_content = re.sub(pattern2, lambda m: f"{m.group(1)}{new_chaos}", new_content)
        
        # Look for std=0.20 or similar patterns
        pattern3 = r'(std\s*=\s*)([0-9]*\.?[0-9]+)'
        new_content = re.sub(pattern3, lambda m: f"{m.group(1)}{new_chaos}", new_content)
        
        print(f"📊 Applied variance adjustment: 0.20 → {new_chaos}")
        return new_content
    
    def apply_home_field_adjustment(self, content: str, adjustment: float) -> str:
        """Adjust home field advantage if needed"""
        # Pattern to find home field advantage
        pattern = r'(home_field_advantage\s*=\s*)([0-9]*\.?[0-9]+)'
        
        def replacement(match):
            current_value = float(match.group(2))
            new_value = current_value + adjustment
            return f"{match.group(1)}{new_value:.3f}"
        
        new_content = re.sub(pattern, replacement, content)
        
        if adjustment != 0:
            print(f"🏠 Applied home field adjustment: {adjustment:+.3f}")
        
        return new_content
    
    def apply_tuning_recommendations(self, recommendations: Dict) -> bool:
        """Apply all tuning recommendations"""
        print("🔧 Applying tuning recommendations...")
        
        # Create backup first
        if not self.create_backup():
            return False
        
        # Read current file
        content = self.read_engine_file()
        if not content:
            return False
        
        # Apply base scoring adjustment
        base_adj = recommendations.get('base_scoring_adjustment', {})
        if 'suggested_base_runs_per_team' in base_adj:
            new_base = base_adj['suggested_base_runs_per_team']
            content = self.apply_base_scoring_adjustment(content, new_base)
        
        # Apply variance adjustment
        var_adj = recommendations.get('variance_adjustment', {})
        if 'suggested_chaos_factor_std' in var_adj:
            new_chaos = var_adj['suggested_chaos_factor_std']
            content = self.apply_variance_adjustment(content, new_chaos)
        
        # Apply home field adjustment if significant
        hfa_adj = recommendations.get('home_field_advantage', {})
        net_advantage = hfa_adj.get('net_home_advantage', 0)
        if abs(net_advantage) > 0.3:
            # Suggest small adjustment
            adjustment = -0.05 if net_advantage > 0 else 0.05
            content = self.apply_home_field_adjustment(content, adjustment)
        
        # Write updated file
        return self.write_engine_file(content)
    
    def generate_test_script(self, recommendations: Dict):
        """Generate a test script to validate the changes"""
        test_content = f'''#!/usr/bin/env python3
"""
Model Tuning Validation Test
Test the updated model parameters against historical data
Generated on: {datetime.now().isoformat()}
"""

from ultra_fast_engine import FastPredictionEngine
from model_performance_analyzer import ModelPerformanceAnalyzer
import json

def test_updated_model():
    """Test the updated model parameters"""
    print("🧪 Testing updated model parameters...")
    
    # Create engine with new parameters
    engine = FastPredictionEngine()
    
    # Test predictions for historical dates
    test_dates = ["2025-08-08", "2025-08-09"]
    
    for date in test_dates:
        print(f"\\n📅 Testing {{date}}...")
        predictions = engine.get_predictions_for_date(date)
        
        if predictions:
            print(f"   ✅ Generated {{len(predictions)}} predictions")
            for game, pred in list(predictions.items())[:2]:  # Show first 2
                total = pred['predicted_away_score'] + pred['predicted_home_score']
                print(f"   🎯 {{game}}: {{pred['predicted_away_score']}}-{{pred['predicted_home_score']}} (total: {{total}})")
        else:
            print(f"   ⚠️ No predictions generated")
    
    # Run performance analysis on updated model
    print("\\n📊 Running performance analysis...")
    analyzer = ModelPerformanceAnalyzer()
    analysis, recommendations = analyzer.run_full_analysis()
    
    if analysis:
        bias = analysis['total_runs_analysis']['bias']
        winner_acc = analysis['winner_prediction']['accuracy']
        
        print(f"\\n🎯 Updated Model Performance:")
        print(f"   • Prediction bias: {{bias:+.2f}} runs (target: ±0.5)")
        print(f"   • Winner accuracy: {{winner_acc:.1%}} (target: 52-58%)")
        
        if abs(bias) <= 0.5:
            print("   ✅ Bias within acceptable range")
        else:
            print("   ⚠️ Bias still needs adjustment")
            
        if 0.52 <= winner_acc <= 0.58:
            print("   ✅ Winner accuracy in target range")
        else:
            print("   ⚠️ Winner accuracy needs improvement")

if __name__ == "__main__":
    test_updated_model()
'''
        
        with open("test_tuned_model.py", "w") as f:
            f.write(test_content)
        
        print("✅ Generated test_tuned_model.py")
    
    def print_summary(self, recommendations: Dict):
        """Print summary of applied changes"""
        print("\\n" + "="*60)
        print("🎯 TUNING SUMMARY")
        print("="*60)
        
        base_adj = recommendations.get('base_scoring_adjustment', {})
        if 'suggested_base_runs_per_team' in base_adj:
            old_base = base_adj.get('current_base_runs_per_team', 3.75)
            new_base = base_adj['suggested_base_runs_per_team']
            print(f"📈 Base scoring: {old_base} → {new_base}")
        
        var_adj = recommendations.get('variance_adjustment', {})
        if 'suggested_chaos_factor_std' in var_adj:
            old_chaos = var_adj.get('current_chaos_factor_std', 0.20)
            new_chaos = var_adj['suggested_chaos_factor_std']
            print(f"🎲 Chaos factor: {old_chaos} → {new_chaos}")
        
        print(f"\\n💾 Backup created: {self.backup_file}")
        print(f"🧪 Test script: test_tuned_model.py")
        print(f"\\n🔄 Next steps:")
        print(f"   1. Run: python test_tuned_model.py")
        print(f"   2. Monitor prediction accuracy")
        print(f"   3. Iterate if needed")

def main():
    """Apply tuning based on analysis results"""
    # Sample recommendations (you can modify these)
    recommendations = {
        'base_scoring_adjustment': {
            'current_base_runs_per_team': 3.75,
            'suggested_base_runs_per_team': 4.30,
            'adjustment_needed': 0.55
        },
        'variance_adjustment': {
            'current_chaos_factor_std': 0.20,
            'suggested_chaos_factor_std': 0.350,
            'variance_ratio': 2.03
        },
        'home_field_advantage': {
            'current_hfa': 0.15,
            'net_home_advantage': 0.2,
            'suggested_adjustment': 'maintain'
        }
    }
    
    tuner = ModelParameterTuner()
    
    print("🚀 Starting model parameter tuning...")
    
    if tuner.apply_tuning_recommendations(recommendations):
        tuner.generate_test_script(recommendations)
        tuner.print_summary(recommendations)
        print("\\n✅ Model tuning completed successfully!")
    else:
        print("\\n❌ Model tuning failed")

if __name__ == "__main__":
    main()
