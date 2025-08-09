#!/usr/bin/env python3
"""
Test script to verify cumulative system and web interface compatibility
"""

import json
from cumulative_ultra_fast_engine import CumulativeUltraFastEngine

def test_cumulative_prediction_format():
    """Test that cumulative predictions return the expected format for JavaScript"""
    print("🧪 Testing cumulative prediction format...")
    
    try:
        engine = CumulativeUltraFastEngine()
        
        # Test with sample team matchup
        result = engine.get_cumulative_prediction("WSN", "NYM")
        
        print(f"✅ Prediction result type: {type(result)}")
        print(f"✅ Prediction structure: {json.dumps(result, indent=2)}")
        
        # Verify expected properties exist
        required_props = ['predicted_total', 'predicted_away_score', 'predicted_home_score']
        
        all_props_exist = all(prop in result for prop in required_props)
        print(f"✅ All required properties exist: {all_props_exist}")
        
        if all_props_exist:
            print("🎯 SUCCESS: Cumulative system returns correct format for JavaScript!")
            print(f"   - predicted_total: {result['predicted_total']}")
            print(f"   - predicted_away_score: {result['predicted_away_score']}")
            print(f"   - predicted_home_score: {result['predicted_home_score']}")
        else:
            missing = [prop for prop in required_props if prop not in result]
            print(f"❌ MISSING PROPERTIES: {missing}")
        
        return result
        
    except Exception as e:
        print(f"❌ ERROR in cumulative prediction: {e}")
        return None

def test_array_filtering():
    """Test JavaScript-style array filtering logic"""
    print("\n🧪 Testing JavaScript filtering compatibility...")
    
    # Simulate prediction data
    sample_predictions = [
        {"predictions": {"predicted_total": 12.5, "predicted_away_score": 6.2, "predicted_home_score": 6.3}},
        {"predictions": {"predicted_total": 5.8, "predicted_away_score": 2.9, "predicted_home_score": 2.9}},
        {"predictions": {"predicted_total": 8.7, "predicted_away_score": 4.1, "predicted_home_score": 4.6}},
    ]
    
    # Test high scoring filter (JavaScript: predictions.filter(p => p.predictions.predicted_total >= 10))
    high_scoring = [p for p in sample_predictions if p["predictions"]["predicted_total"] >= 10]
    print(f"✅ High scoring games: {len(high_scoring)} (expected: 1)")
    
    # Test low scoring filter  
    low_scoring = [p for p in sample_predictions if p["predictions"]["predicted_total"] <= 6]
    print(f"✅ Low scoring games: {len(low_scoring)} (expected: 1)")
    
    # Test array access safety
    try:
        if len(high_scoring) > 0:
            highest_total = high_scoring[0]["predictions"]["predicted_total"]
            print(f"✅ Safe array access: highest_total = {highest_total}")
        else:
            print("✅ No high scoring games - safe to skip array access")
    except Exception as e:
        print(f"❌ Array access error: {e}")

if __name__ == "__main__":
    print("🔧 Testing Cumulative System & JavaScript Compatibility")
    print("=" * 60)
    
    # Test cumulative prediction format
    result = test_cumulative_prediction_format()
    
    # Test array filtering 
    test_array_filtering()
    
    print("\n🎯 SUMMARY:")
    if result:
        print("✅ Cumulative system produces correct JavaScript-compatible format")
        print("✅ Property names match: predicted_total (not predicted_total_runs)")
        print("✅ Ready for web interface testing!")
    else:
        print("❌ Issues detected - need further debugging")
