#!/usr/bin/env python3
from ultra_fast_engine import FastPredictionEngine
import json

engine = FastPredictionEngine()
result = engine.get_fast_prediction("Yankees", "Red Sox", sim_count=1000)

print("PREDICTION RESULT STRUCTURE:")
print("=" * 40)
print(json.dumps(result, indent=2))
