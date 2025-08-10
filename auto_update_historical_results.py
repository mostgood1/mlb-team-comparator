#!/usr/bin/env python3
"""
Historical Results Auto-Updater
Automatically fetches completed MLB game results and updates historical cache
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class HistoricalResultsUpdater:
    """Updates historical predictions cache with real game results"""
    
    def __init__(self):
        self.cache_file = "historical_predictions_cache.json"
        self.base_url = "https://statsapi.mlb.com/api/v1"
        
    def fetch_completed_games_for_date(self, date_str: str) -> List[Dict]:
        """Fetch completed games for a specific date from MLB API"""
        try:
            # Format date for MLB API
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%m/%d/%Y")
            
            # Fetch schedule for the date
            schedule_url = f"{self.base_url}/schedule?sportId=1&date={formatted_date}"
            
            print(f"🔍 Fetching games for {date_str}...")
            response = requests.get(schedule_url, timeout=10)
            response.raise_for_status()
            
            schedule_data = response.json()
            completed_games = []
            
            if 'dates' in schedule_data and schedule_data['dates']:
                for date_entry in schedule_data['dates']:
                    if 'games' in date_entry:
                        for game in date_entry['games']:
                            # Only process completed games
                            if game.get('status', {}).get('statusCode') == 'F':
                                game_info = self._extract_game_info(game)
                                if game_info:
                                    completed_games.append(game_info)
            
            print(f"✅ Found {len(completed_games)} completed games for {date_str}")
            return completed_games
            
        except Exception as e:
            print(f"❌ Error fetching games for {date_str}: {e}")
            return []
    
    def _extract_game_info(self, game: Dict) -> Optional[Dict]:
        """Extract relevant game information"""
        try:
            teams = game.get('teams', {})
            away_team = teams.get('away', {})
            home_team = teams.get('home', {})
            
            # Get team names
            away_name = away_team.get('team', {}).get('name', '')
            home_name = home_team.get('team', {}).get('name', '')
            
            # Get scores
            away_score = away_team.get('score', 0)
            home_score = home_team.get('score', 0)
            
            if not away_name or not home_name:
                return None
                
            return {
                'away_team': away_name,
                'home_team': home_name,
                'away_score': away_score,
                'home_score': home_score,
                'total_score': away_score + home_score,
                'game_id': game.get('gamePk', ''),
                'date': game.get('gameDate', '')
            }
            
        except Exception as e:
            print(f"❌ Error extracting game info: {e}")
            return None
    
    def load_cache(self) -> Dict:
        """Load existing historical cache"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"❌ Error loading cache: {e}")
        return {}
    
    def save_cache(self, cache_data: Dict):
        """Save updated cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            print(f"💾 Updated {self.cache_file}")
        except Exception as e:
            print(f"❌ Error saving cache: {e}")
    
    def update_historical_results_for_date(self, date_str: str) -> bool:
        """Update historical results for a specific date"""
        # Fetch completed games
        completed_games = self.fetch_completed_games_for_date(date_str)
        
        if not completed_games:
            print(f"ℹ️ No completed games found for {date_str}")
            return False
        
        # Load existing cache
        cache = self.load_cache()
        
        # Ensure date entry exists
        if date_str not in cache:
            cache[date_str] = {
                'cached_predictions': {},
                'last_updated': datetime.now().isoformat()
            }
        
        # Update with real results
        predictions = cache[date_str].get('cached_predictions', {})
        
        for game in completed_games:
            # Create game key (similar to prediction system)
            game_key = f"{game['away_team']} @ {game['home_team']}"
            
            # Update or create entry
            if game_key in predictions:
                # Update existing prediction with actual results
                predictions[game_key].update({
                    'actual_away_score': game['away_score'],
                    'actual_home_score': game['home_score'],
                    'actual_total_score': game['total_score'],
                    'has_real_results': True,
                    'updated_timestamp': datetime.now().isoformat()
                })
                
                # Calculate prediction error if we have predictions
                if all(key in predictions[game_key] for key in ['predicted_away_score', 'predicted_home_score']):
                    pred_away = predictions[game_key]['predicted_away_score']
                    pred_home = predictions[game_key]['predicted_home_score']
                    pred_total = pred_away + pred_home
                    
                    predictions[game_key].update({
                        'prediction_error_away': abs(pred_away - game['away_score']),
                        'prediction_error_home': abs(pred_home - game['home_score']),
                        'prediction_error_total': abs(pred_total - game['total_score']),
                        'winner_predicted_correctly': self._check_winner_prediction(
                            pred_away, pred_home, game['away_score'], game['home_score']
                        )
                    })
                
                print(f"✅ Updated: {game_key} -> {game['away_score']}-{game['home_score']}")
            else:
                # Create new entry with just actual results
                predictions[game_key] = {
                    'actual_away_score': game['away_score'],
                    'actual_home_score': game['home_score'],
                    'actual_total_score': game['total_score'],
                    'has_real_results': True,
                    'no_prediction_available': True,
                    'updated_timestamp': datetime.now().isoformat()
                }
                print(f"📝 Added new: {game_key} -> {game['away_score']}-{game['home_score']}")
        
        # Update cache
        cache[date_str]['cached_predictions'] = predictions
        cache[date_str]['last_updated'] = datetime.now().isoformat()
        
        # Save updated cache
        self.save_cache(cache)
        
        return True
    
    def _check_winner_prediction(self, pred_away: int, pred_home: int, actual_away: int, actual_home: int) -> bool:
        """Check if we predicted the winner correctly"""
        predicted_winner = 'home' if pred_home > pred_away else 'away'
        actual_winner = 'home' if actual_home > actual_away else 'away'
        return predicted_winner == actual_winner
    
    def auto_update_recent_dates(self, days_back: int = 3) -> int:
        """Auto-update historical results for recent dates"""
        updated_count = 0
        current_date = datetime.now()
        
        for i in range(days_back):
            check_date = current_date - timedelta(days=i+1)
            date_str = check_date.strftime("%Y-%m-%d")
            
            print(f"\n🔄 Checking {date_str}...")
            if self.update_historical_results_for_date(date_str):
                updated_count += 1
        
        return updated_count

def main():
    """Test the historical results updater"""
    updater = HistoricalResultsUpdater()
    
    # Update recent dates
    print("🚀 Auto-updating recent historical results...")
    updated = updater.auto_update_recent_dates(3)
    print(f"\n✅ Updated {updated} dates with real results")

if __name__ == "__main__":
    main()
