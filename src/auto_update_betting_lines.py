#!/usr/bin/env python3
"""
MLB Betting Lines Auto-Fetcher
Integrated into the auto-refresh system for enterprise-grade betting lines management
"""

import requests
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class BettingLinesAutoUpdater:
    """Auto-updates MLB betting lines with intelligent caching and error handling"""
    
    def __init__(self):
        self.odds_api_key = '07da97d86f1b1e431b4e01341abbf9e2'
        self.odds_api_url = 'https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/'
        self.betting_lines_file = 'mlb_betting_lines.json'
        
    def should_update_betting_lines(self, max_age_hours: int = 3) -> bool:
        """Check if betting lines need updating based on age"""
        try:
            if not os.path.exists(self.betting_lines_file):
                print("📊 No betting lines file found - needs initial fetch")
                return True
                
            file_age = time.time() - os.path.getmtime(self.betting_lines_file)
            max_age_seconds = max_age_hours * 3600
            
            if file_age > max_age_seconds:
                print(f"📅 Betting lines are {file_age/3600:.1f} hours old (max: {max_age_hours}h) - needs update")
                return True
            else:
                print(f"✅ Betting lines are fresh ({file_age/3600:.1f} hours old)")
                return False
                
        except Exception as e:
            print(f"⚠️ Error checking betting lines age: {e}")
            return True
    
    def fetch_betting_lines_for_date(self, date_str: str) -> Dict:
        """
        Fetch betting lines for all MLB games for a given date using the Odds-API.
        Returns a dict: { 'matchup_key': { 'moneyline': {...}, 'runline': {...}, 'total': {...} } }
        """
        print(f"🎯 Fetching betting lines from Odds-API...")
        
        params = {
            'apiKey': self.odds_api_key,
            'regions': 'us',
            'markets': 'h2h,spreads,totals',
            'oddsFormat': 'american',
            'dateFormat': 'iso',
        }
        
        try:
            resp = requests.get(self.odds_api_url, params=params, timeout=20)
            resp.raise_for_status()
            games = resp.json()
            
            lines = {}
            for game in games:
                home = game.get('home_team')
                away = game.get('away_team')
                if not home or not away:
                    continue
                    
                matchup_key = f"{away}_at_{home}"
                moneyline = None
                runline = None
                total = None
                
                # Each bookmaker has odds for h2h (moneyline), spreads (runline), totals (over/under)
                # We'll use the first bookmaker's odds as representative
                bookmakers = game.get('bookmakers', [])
                if bookmakers:
                    markets = {m['key']: m for m in bookmakers[0].get('markets', [])}
                    
                    # Moneyline (h2h)
                    h2h = markets.get('h2h')
                    if h2h and 'outcomes' in h2h:
                        moneyline = {o['name']: o['price'] for o in h2h['outcomes']}
                    
                    # Runline (spreads)
                    spreads = markets.get('spreads')
                    if spreads and 'outcomes' in spreads:
                        runline = [{
                            'team': o['name'],
                            'point': o.get('point'),
                            'price': o.get('price')
                        } for o in spreads['outcomes']]
                    
                    # Total (totals)
                    totals = markets.get('totals')
                    if totals and 'outcomes' in totals:
                        total = [{
                            'name': o['name'],
                            'point': o.get('point'),
                            'price': o.get('price')
                        } for o in totals['outcomes']]
                
                lines[matchup_key] = {
                    'moneyline': moneyline,
                    'runline': runline,
                    'total': total
                }
            
            print(f"✅ Successfully fetched betting lines for {len(lines)} games")
            return lines
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error fetching betting lines: {e}")
            raise
        except Exception as e:
            print(f"❌ Error processing betting lines: {e}")
            raise
    
    def load_existing_lines(self) -> Dict:
        """Load existing betting lines from JSON cache"""
        if os.path.exists(self.betting_lines_file):
            try:
                with open(self.betting_lines_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error reading existing betting lines: {e}")
                return {}
        return {}
    
    def save_lines(self, data: Dict) -> None:
        """Save betting lines to JSON cache"""
        try:
            with open(self.betting_lines_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Betting lines saved to {self.betting_lines_file}")
        except Exception as e:
            print(f"❌ Error saving betting lines: {e}")
            raise
    
    def update_betting_lines(self) -> bool:
        """Update betting lines for current and recent games"""
        print("\n🎲 UPDATING BETTING LINES")
        print("-" * 40)
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Load existing data
            data = self.load_existing_lines()
            
            success_count = 0
            total_attempts = 0
            
            # Update today's lines (always refresh)
            try:
                print(f"📅 Updating betting lines for today ({today})...")
                today_lines = self.fetch_betting_lines_for_date(today)
                data[today] = today_lines
                success_count += 1
                
                # Check coverage
                try:
                    from TodaysGames import get_games_for_date
                    today_games = get_games_for_date(today)
                    if today_games:
                        today_matchups = set(f"{g['away']}_at_{g['home']}" for g in today_games if 'away' in g and 'home' in g)
                        missing_today = today_matchups - set(today_lines.keys())
                        if missing_today:
                            print(f"⚠️ Missing odds for {len(missing_today)} today's matchups: {sorted(list(missing_today)[:3])}...")
                        else:
                            print(f"✅ Complete coverage for all {len(today_matchups)} today's games")
                except Exception as e:
                    print(f"⚠️ Could not verify game coverage: {e}")
                    
            except Exception as e:
                print(f"❌ Failed to update today's betting lines: {e}")
            total_attempts += 1
            
            # Update tomorrow's lines (for pre-game betting)
            try:
                print(f"📅 Updating betting lines for tomorrow ({tomorrow})...")
                tomorrow_lines = self.fetch_betting_lines_for_date(tomorrow)
                if tomorrow_lines:
                    data[tomorrow] = tomorrow_lines
                    success_count += 1
                    print(f"✅ Updated betting lines for {len(tomorrow_lines)} tomorrow's games")
                else:
                    print("ℹ️ No games scheduled for tomorrow")
            except Exception as e:
                print(f"⚠️ Could not fetch tomorrow's betting lines: {e}")
            total_attempts += 1
            
            # Clean old data (keep last 30 days)
            cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            old_dates = [date for date in data.keys() if date < cutoff_date]
            for old_date in old_dates:
                del data[old_date]
            
            if old_dates:
                print(f"🧹 Cleaned {len(old_dates)} old betting line entries")
            
            # Save updated data
            self.save_lines(data)
            
            print(f"\n📊 BETTING LINES UPDATE RESULTS:")
            print(f"   ✅ Successful updates: {success_count}/{total_attempts}")
            print(f"   📅 Total dates with lines: {len(data)}")
            print(f"   🎯 Games with lines today: {len(data.get(today, {}))}")
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Critical error updating betting lines: {e}")
            return False
    
    def get_api_usage_info(self) -> str:
        """Get information about API usage and limits"""
        return f"🔗 Using Odds-API (Key: ...{self.odds_api_key[-4:]}) - Limited requests per month"

def test_betting_lines_updater():
    """Test the betting lines updater"""
    print("🧪 Testing Betting Lines Auto-Updater")
    print("=" * 50)
    
    updater = BettingLinesAutoUpdater()
    
    # Test update check
    should_update = updater.should_update_betting_lines()
    print(f"Should update: {should_update}")
    
    # Test update
    if updater.update_betting_lines():
        print("✅ Betting lines update test successful!")
    else:
        print("❌ Betting lines update test failed!")

if __name__ == "__main__":
    test_betting_lines_updater()
