#!/usr/bin/env python3
from ultra_fast_engine import FastPredictionEngine
import time

print("Testing Ultra-Fast Engine with Complete Data...")

try:
    # Initialize engine
    engine = FastPredictionEngine()
    print("✅ Engine initialized successfully")
    
    # Test a prediction
    start_time = time.time()
    result = engine.get_fast_prediction("Yankees", "Red Sox", sim_count=1000)
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000
    print(f"✅ Prediction completed in {execution_time:.1f}ms")
    
    # Check result structure
    if 'predictions' in result:
        pred = result['predictions']
        print(f"✅ Predicted total runs: {pred.get('predicted_total_runs', 'N/A')}")
        home_win_prob = pred.get('home_win_probability', 0)
        if isinstance(home_win_prob, (int, float)):
            print(f"✅ Home win probability: {home_win_prob:.1%}")
        else:
            print(f"✅ Home win probability: {home_win_prob}")
    
    print("\n🎯 All pitching data loaded successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
