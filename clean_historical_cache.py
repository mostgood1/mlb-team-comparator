#!/usr/bin/env python3
"""
Clean Historical Cache - Remove Test Data
Keep only real MLB games fetched from the API
"""

import json
from datetime import datetime

def clean_historical_cache():
    """Remove test data and keep only real MLB games"""
    
    cache_file = "historical_predictions_cache.json"
    backup_file = f"historical_predictions_cache_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        # Load current cache
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        # Create backup
        with open(backup_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Created backup: {backup_file}")
        
        cleaned_data = {}
        total_games_before = 0
        total_games_after = 0
        
        # Process each date
        for date, date_data in data.items():
            if 'cached_predictions' not in date_data:
                continue
                
            games_before = len(date_data['cached_predictions'])
            total_games_before += games_before
            
            cleaned_games = {}
            
            # Keep only games with recent timestamps (real API fetches)
            for game_key, game_data in date_data['cached_predictions'].items():
                timestamp = game_data.get('updated_timestamp', '')
                
                # Keep games updated recently (2025-08-10) - these are real API fetches
                if '2025-08-10' in timestamp:
                    cleaned_games[game_key] = game_data
                    print(f"✅ Kept real game: {game_key} ({timestamp})")
                else:
                    print(f"❌ Removed test data: {game_key} ({timestamp})")
            
            if cleaned_games:
                cleaned_data[date] = {
                    'cached_predictions': cleaned_games,
                    'last_updated': datetime.now().isoformat()
                }
                games_after = len(cleaned_games)
                total_games_after += games_after
                print(f"📅 {date}: {games_before} → {games_after} games")
        
        # Save cleaned data
        with open(cache_file, 'w') as f:
            json.dump(cleaned_data, f, indent=2)
        
        print(f"\\n🧹 Cleaning Summary:")
        print(f"   • Total games before: {total_games_before}")
        print(f"   • Total games after: {total_games_after}")
        print(f"   • Removed: {total_games_before - total_games_after} test games")
        print(f"   • Kept: {total_games_after} real MLB games")
        print(f"\\n✅ Historical cache cleaned successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning cache: {e}")
        return False

if __name__ == "__main__":
    clean_historical_cache()
