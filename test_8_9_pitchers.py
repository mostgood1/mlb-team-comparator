"""
Test updated pitcher data for 8/9
"""
from ultra_fast_engine import FastPredictionEngine

engine = FastPredictionEngine()
print("🏟️ Testing today's games (8/9) with updated pitchers:")

# Test the first game - Miami Marlins @ Atlanta Braves
prediction = engine.get_fast_prediction('Miami Marlins', 'Atlanta Braves')
pitcher_quality = prediction.get('pitcher_quality', {})

print(f"Game: Miami Marlins @ Atlanta Braves")
print(f"Away Pitcher: {pitcher_quality.get('away_pitcher_name', 'Unknown')}")
print(f"Home Pitcher: {pitcher_quality.get('home_pitcher_name', 'Unknown')}")
print(f"Expected for 8/9: Sandy Alcantara vs Erick Fedde")

# Test another game
prediction2 = engine.get_fast_prediction('Houston Astros', 'New York Yankees')
pitcher_quality2 = prediction2.get('pitcher_quality', {})

print(f"\nGame: Houston Astros @ New York Yankees")
print(f"Away Pitcher: {pitcher_quality2.get('away_pitcher_name', 'Unknown')}")
print(f"Home Pitcher: {pitcher_quality2.get('home_pitcher_name', 'Unknown')}")
print(f"Expected for 8/9: Framber Valdez vs Luis Gil")

# Test Washington @ San Francisco
prediction3 = engine.get_fast_prediction('Washington Nationals', 'San Francisco Giants')
pitcher_quality3 = prediction3.get('pitcher_quality', {})

print(f"\nGame: Washington Nationals @ San Francisco Giants")
print(f"Away Pitcher: {pitcher_quality3.get('away_pitcher_name', 'Unknown')}")
print(f"Home Pitcher: {pitcher_quality3.get('home_pitcher_name', 'Unknown')}")
print(f"Expected for 8/9: Brad Lord vs Carson Whisenhunt")
