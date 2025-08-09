"""
Test pitcher data for today's games
"""
from ultra_fast_engine import FastPredictionEngine

engine = FastPredictionEngine()
print("🏟️ Testing today's games with correct pitchers:")

# Test the first game - Cincinnati Reds @ Pittsburgh Pirates
prediction = engine.get_fast_prediction('Cincinnati Reds', 'Pittsburgh Pirates')
pitcher_quality = prediction.get('pitcher_quality', {})

print(f"Game: Cincinnati Reds @ Pittsburgh Pirates")
print(f"Away Pitcher: {pitcher_quality.get('away_pitcher_name', 'Unknown')}")
print(f"Home Pitcher: {pitcher_quality.get('home_pitcher_name', 'Unknown')}")
print(f"Expected: Chase Burns vs Mitch Keller")

# Test another game
prediction2 = engine.get_fast_prediction('Houston Astros', 'New York Yankees')
pitcher_quality2 = prediction2.get('pitcher_quality', {})

print(f"\nGame: Houston Astros @ New York Yankees")
print(f"Away Pitcher: {pitcher_quality2.get('away_pitcher_name', 'Unknown')}")
print(f"Home Pitcher: {pitcher_quality2.get('home_pitcher_name', 'Unknown')}")
print(f"Expected: Hunter Brown vs Cam Schlittler")
