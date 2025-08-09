#!/usr/bin/env python3
"""
Auto-Update Pitcher Stats and Team Strength Data
Fetches fresh 2025 MLB data and calculates updated team strengths
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import time
from auto_update_betting_lines import BettingLinesAutoUpdater

class MLBDataAutoUpdater:
    
    def __init__(self):
        self.current_season = 2025
        self.base_url = "https://statsapi.mlb.com/api/v1"
        self.betting_updater = BettingLinesAutoUpdater()
        
    def should_update_data(self, filename: str, max_age_hours: int = 24) -> bool:
        """Check if data file needs updating based on age"""
        try:
            if not os.path.exists(filename):
                return True
                
            file_age = time.time() - os.path.getmtime(filename)
            max_age_seconds = max_age_hours * 3600
            
            if file_age > max_age_seconds:
                print(f"📅 {filename} is {file_age/3600:.1f} hours old (max: {max_age_hours}h) - needs update")
                return True
            else:
                print(f"✅ {filename} is fresh ({file_age/3600:.1f} hours old)")
                return False
                
        except Exception as e:
            print(f"⚠️ Error checking {filename} age: {e}")
            return True

    def fetch_team_stats(self) -> Dict:
        """Fetch current season team statistics"""
        print("📊 Fetching 2025 team statistics...")
        
        try:
            # Get team standings for win percentages
            url = f"{self.base_url}/standings?leagueId=103,104&season={self.current_season}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            standings_data = response.json()
            
            team_stats = {}
            
            for league in standings_data.get('records', []):
                for team_record in league.get('teamRecords', []):
                    team = team_record.get('team', {})
                    team_name = team.get('name', '')
                    
                    # Calculate strength based on win percentage and recent performance
                    wins = team_record.get('wins', 0)
                    losses = team_record.get('losses', 0)
                    total_games = wins + losses
                    
                    if total_games > 0:
                        win_pct = wins / total_games
                        
                        # Convert win percentage to strength scale (-0.3 to +0.3)
                        # .500 = 0.0 strength, .600 = +0.2, .400 = -0.2
                        strength = (win_pct - 0.5) * 0.6  # Scale to ±0.3 range
                        
                        team_stats[team_name] = {
                            'wins': wins,
                            'losses': losses,
                            'win_pct': win_pct,
                            'strength': round(strength, 3),
                            'games_back': team_record.get('gamesBack', '0'),
                            'last_updated': datetime.now().isoformat()
                        }
            
            print(f"✅ Fetched stats for {len(team_stats)} teams")
            return team_stats
            
        except Exception as e:
            print(f"❌ Error fetching team stats: {e}")
            return {}

    def fetch_pitcher_stats(self) -> Dict:
        """Fetch current season pitcher statistics"""
        print("⚾ Fetching 2025 pitcher statistics...")
        
        try:
            # Get all teams first
            teams_url = f"{self.base_url}/teams?sportId=1&season={self.current_season}"
            teams_response = requests.get(teams_url, timeout=15)
            teams_response.raise_for_status()
            teams_data = teams_response.json()
            
            all_pitcher_stats = {}
            
            for team in teams_data.get('teams', []):
                team_id = team.get('id')
                team_name = team.get('name')
                
                print(f"  📈 Fetching {team_name} pitchers...")
                
                # Get team roster
                roster_url = f"{self.base_url}/teams/{team_id}/roster?season={self.current_season}"
                roster_response = requests.get(roster_url, timeout=10)
                
                if roster_response.status_code == 200:
                    roster_data = roster_response.json()
                    
                    for player in roster_data.get('roster', []):
                        person = player.get('person', {})
                        position = player.get('position', {})
                        
                        # Only process pitchers
                        if position.get('abbreviation') in ['P', 'SP', 'RP', 'CP']:
                            player_id = person.get('id')
                            player_name = person.get('fullName')
                            
                            if player_id and player_name:
                                # Get pitcher stats
                                stats_url = f"{self.base_url}/people/{player_id}/stats?stats=season&season={self.current_season}&group=pitching"
                                
                                try:
                                    stats_response = requests.get(stats_url, timeout=8)
                                    if stats_response.status_code == 200:
                                        stats_data = stats_response.json()
                                        
                                        for stat_group in stats_data.get('stats', []):
                                            for split in stat_group.get('splits', []):
                                                stat = split.get('stat', {})
                                                
                                                all_pitcher_stats[str(player_id)] = {
                                                    'name': player_name,
                                                    'team': team_name,
                                                    'era': float(stat.get('era', 4.50)),
                                                    'whip': float(stat.get('whip', 1.30)),
                                                    'strikeouts': int(stat.get('strikeOuts', 0)),
                                                    'walks': int(stat.get('baseOnBalls', 0)),
                                                    'innings_pitched': float(stat.get('inningsPitched', 0)),
                                                    'games_started': int(stat.get('gamesStarted', 0)),
                                                    'wins': int(stat.get('wins', 0)),
                                                    'losses': int(stat.get('losses', 0)),
                                                    'last_updated': datetime.now().isoformat()
                                                }
                                                break  # Only need the first (season) stats
                                                
                                except Exception as e:
                                    print(f"    ⚠️ Error fetching {player_name} stats: {e}")
                                    continue
                
                # Small delay to be nice to the API
                time.sleep(0.1)
            
            print(f"✅ Fetched stats for {len(all_pitcher_stats)} pitchers")
            return all_pitcher_stats
            
        except Exception as e:
            print(f"❌ Error fetching pitcher stats: {e}")
            return {}

    def update_team_strength_cache(self) -> bool:
        """Update team strength cache with fresh data"""
        if not self.should_update_data('team_strength_cache.json', max_age_hours=12):
            return True
            
        print("🔄 Updating team strength cache...")
        
        team_stats = self.fetch_team_stats()
        if not team_stats:
            print("❌ Failed to fetch team stats")
            return False
        
        # Create simplified strength cache
        strength_cache = {}
        for team_name, stats in team_stats.items():
            strength_cache[team_name] = stats['strength']
        
        # Save to file
        try:
            with open('team_strength_cache.json', 'w') as f:
                json.dump(strength_cache, f, indent=2)
            
            print(f"💾 Updated team_strength_cache.json with {len(strength_cache)} teams")
            
            # Show some examples
            sorted_teams = sorted(strength_cache.items(), key=lambda x: x[1], reverse=True)
            print("📊 Top 5 teams by strength:")
            for team, strength in sorted_teams[:5]:
                print(f"   {team}: {strength:+.3f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving team strength cache: {e}")
            return False

    def update_pitcher_stats(self) -> bool:
        """Update pitcher stats file with fresh 2025 data"""
        if not self.should_update_data('pitcher_stats_2025_and_career.json', max_age_hours=24):
            return True
            
        print("🔄 Updating pitcher stats...")
        
        pitcher_stats = self.fetch_pitcher_stats()
        if not pitcher_stats:
            print("❌ Failed to fetch pitcher stats")
            return False
        
        # Load existing data if available (to preserve career stats)
        existing_data = {}
        if os.path.exists('pitcher_stats_2025_and_career.json'):
            try:
                with open('pitcher_stats_2025_and_career.json', 'r') as f:
                    existing_data = json.load(f)
                print(f"📚 Loaded {len(existing_data)} existing pitcher records")
            except Exception as e:
                print(f"⚠️ Could not load existing data: {e}")
        
        # Merge new 2025 stats with existing career data
        merged_data = existing_data.copy()
        updated_count = 0
        
        for pitcher_id, new_stats in pitcher_stats.items():
            if pitcher_id in merged_data:
                # Update 2025 stats while preserving career data
                merged_data[pitcher_id].update(new_stats)
                updated_count += 1
            else:
                # New pitcher
                merged_data[pitcher_id] = new_stats
                updated_count += 1
        
        # Save updated data
        try:
            with open('pitcher_stats_2025_and_career.json', 'w') as f:
                json.dump(merged_data, f, indent=2)
            
            print(f"💾 Updated pitcher_stats_2025_and_career.json")
            print(f"   Total pitchers: {len(merged_data)}")
            print(f"   Updated records: {updated_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving pitcher stats: {e}")
            return False
    
    def update_betting_lines(self) -> bool:
        """Update betting lines using the integrated betting lines updater"""
        try:
            # Check if betting lines need updating (every 3 hours)
            if not self.betting_updater.should_update_betting_lines(max_age_hours=3):
                print("✅ Betting lines are fresh - skipping update")
                return True
            
            # Update betting lines
            return self.betting_updater.update_betting_lines()
            
        except Exception as e:
            print(f"❌ Error updating betting lines: {e}")
            return False

    def update_all_data(self) -> bool:
        """Update all MLB data files including betting lines"""
        print("🚀 AUTO-UPDATING MLB DATA")
        print("=" * 40)
        
        success_count = 0
        total_updates = 3  # Added betting lines
        
        # Update team strengths
        if self.update_team_strength_cache():
            success_count += 1
        
        # Update pitcher stats
        if self.update_pitcher_stats():
            success_count += 1
        
        # Update betting lines (new)
        if self.update_betting_lines():
            success_count += 1
        
        print("\n" + "=" * 40)
        print(f"📊 RESULTS: {success_count}/{total_updates} updates successful")
        
        if success_count == total_updates:
            print("🎉 All MLB data updated successfully!")
            return True
        else:
            print("⚠️ Some updates failed")
            return False

def main():
    """Main execution function"""
    updater = MLBDataAutoUpdater()
    updater.update_all_data()

if __name__ == "__main__":
    main()
