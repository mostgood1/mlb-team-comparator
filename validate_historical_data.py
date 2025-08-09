"""
Historical data validation tool to identify date mismatches in pitcher data
"""

import json
import os
from datetime import datetime, timedelta

def validate_historical_pitcher_data():
    """Check if historical pitcher data contains date mismatches"""
    
    starters_file = 'ProjectedStarters.json'
    if not os.path.exists(starters_file):
        print("❌ ProjectedStarters.json not found")
        return
    
    print("🔍 Validating historical pitcher data for date accuracy...")
    
    with open(starters_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Found {len(data)} total matchups in ProjectedStarters.json")
    
    # For demonstration, let's check what we have
    sample_matchups = list(data.items())[:5]
    print("\n📋 Sample current matchups:")
    for matchup, details in sample_matchups:
        away_starter = details.get('away_starter', 'TBD')
        home_starter = details.get('home_starter', 'TBD')
        print(f"   {matchup}")
        print(f"     Away: {away_starter}")
        print(f"     Home: {home_starter}")
    
    # The issue: We need a way to store date metadata with each matchup
    # Current structure doesn't include dates, making validation difficult
    print("\n⚠️ Analysis: Current data structure lacks date metadata")
    print("   This makes it impossible to validate historical accuracy")
    print("   Recommendation: Implement date-aware storage structure")
    
    return data

def recommend_improved_structure():
    """Show recommended structure for date-aware pitcher data"""
    
    print("\n💡 Recommended improved data structure:")
    print("""
    {
        "2025-08-08": {
            "Miami Marlins at Atlanta Braves": {
                "away_starter": "Jesus Luzardo",
                "home_starter": "Spencer Schwellenbach"
            }
        },
        "2025-08-09": {
            "Miami Marlins at Atlanta Braves": {
                "away_starter": "Sandy Alcantara", 
                "home_starter": "Erick Fedde"
            }
        }
    }
    """)
    
    print("✅ Benefits of date-aware structure:")
    print("   - Prevents cross-date contamination")
    print("   - Enables historical validation")
    print("   - Supports date-specific queries")
    print("   - Maintains data integrity")

if __name__ == "__main__":
    validate_historical_pitcher_data()
    recommend_improved_structure()
