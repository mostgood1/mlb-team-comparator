"""
Cumulative Simulation Data Manager
Accumulates simulation data over time instead of starting from scratch on each reload
"""

import json
import os
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class CumulativeGameData:
    """Stores cumulative simulation data for a specific game"""
    away_team: str
    home_team: str
    date: str
    total_simulations: int = 0
    away_wins: int = 0
    home_wins: int = 0
    total_away_runs: int = 0
    total_home_runs: int = 0
    first_simulation: str = None  # timestamp
    last_simulation: str = None   # timestamp
    confidence_level: float = 0.0
    
    def add_simulation_batch(self, batch_results: List[Dict]):
        """Add a batch of simulation results to cumulative data"""
        now = datetime.now().isoformat()
        
        if self.first_simulation is None:
            self.first_simulation = now
        self.last_simulation = now
        
        for result in batch_results:
            self.total_simulations += 1
            away_score = result.get('away_score', 0)
            home_score = result.get('home_score', 0)
            
            self.total_away_runs += away_score
            self.total_home_runs += home_score
            
            if home_score > away_score:
                self.home_wins += 1
            else:
                self.away_wins += 1
        
        # Update confidence level based on sample size
        self.confidence_level = min(95.0, (self.total_simulations / 10000) * 100)
    
    @property
    def home_win_probability(self) -> float:
        """Calculate home team win probability"""
        if self.total_simulations == 0:
            return 0.5
        return round(self.home_wins / self.total_simulations, 4)
    
    @property
    def away_win_probability(self) -> float:
        """Calculate away team win probability"""
        return round(1.0 - self.home_win_probability, 4)
    
    @property
    def average_home_runs(self) -> float:
        """Average runs per game for home team"""
        if self.total_simulations == 0:
            return 4.5
        return self.total_home_runs / self.total_simulations
    
    @property
    def average_away_runs(self) -> float:
        """Average runs per game for away team"""
        if self.total_simulations == 0:
            return 4.3
        return self.total_away_runs / self.total_simulations

class CumulativeSimulationManager:
    """Manages cumulative simulation data across reloads"""
    
    def __init__(self, data_file: str = "cumulative_simulations.json"):
        self.data_file = data_file
        self.game_data: Dict[str, CumulativeGameData] = {}
        self.load_existing_data()
    
    def _get_game_key(self, away_team: str, home_team: str, date: str) -> str:
        """Generate unique key for a game"""
        return f"{date}_{away_team}_vs_{home_team}"
    
    def load_existing_data(self):
        """Load existing cumulative data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for key, game_dict in data.items():
                    self.game_data[key] = CumulativeGameData(**game_dict)
                
                print(f"📊 Loaded cumulative data for {len(self.game_data)} games")
            except Exception as e:
                print(f"⚠️ Error loading cumulative data: {e}")
                self.game_data = {}
        else:
            print("📊 Starting fresh cumulative simulation database")
    
    def save_data(self):
        """Save cumulative data to file"""
        try:
            # Convert dataclasses to dictionaries
            data_to_save = {}
            for key, game_data in self.game_data.items():
                data_to_save[key] = asdict(game_data)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved cumulative data for {len(self.game_data)} games")
        except Exception as e:
            print(f"❌ Error saving cumulative data: {e}")
    
    def add_simulation_batch(self, away_team: str, home_team: str, date: str, 
                           batch_results: List[Dict]) -> CumulativeGameData:
        """Add new simulation batch to cumulative data"""
        game_key = self._get_game_key(away_team, home_team, date)
        
        if game_key not in self.game_data:
            self.game_data[game_key] = CumulativeGameData(
                away_team=away_team,
                home_team=home_team,
                date=date
            )
        
        self.game_data[game_key].add_simulation_batch(batch_results)
        
        # Auto-save after each batch
        self.save_data()
        
        return self.game_data[game_key]
    
    def get_game_data(self, away_team: str, home_team: str, date: str) -> Optional[CumulativeGameData]:
        """Get cumulative data for a specific game"""
        game_key = self._get_game_key(away_team, home_team, date)
        return self.game_data.get(game_key)
    
    def should_run_more_simulations(self, away_team: str, home_team: str, date: str, 
                                  target_simulations: int = 10000) -> Tuple[bool, int]:
        """Determine if more simulations are needed and how many"""
        game_data = self.get_game_data(away_team, home_team, date)
        
        if game_data is None:
            return True, target_simulations
        
        current_sims = game_data.total_simulations
        if current_sims < target_simulations:
            needed = min(1500, target_simulations - current_sims)  # Batch size of 1500
            return True, needed
        
        return False, 0
    
    def get_simulation_summary(self) -> Dict:
        """Get summary of all cumulative simulation data"""
        if not self.game_data:
            return {"total_games": 0, "total_simulations": 0}
        
        total_simulations = sum(game.total_simulations for game in self.game_data.values())
        games_by_date = {}
        
        for game in self.game_data.values():
            date = game.date
            if date not in games_by_date:
                games_by_date[date] = []
            games_by_date[date].append({
                "matchup": f"{game.away_team} @ {game.home_team}",
                "simulations": game.total_simulations,
                "confidence": f"{game.confidence_level:.1f}%",
                "home_win_prob": f"{game.home_win_probability:.1%}"
            })
        
        return {
            "total_games": len(self.game_data),
            "total_simulations": total_simulations,
            "average_sims_per_game": total_simulations / len(self.game_data) if self.game_data else 0,
            "games_by_date": games_by_date
        }
    
    def cleanup_old_data(self, days_to_keep: int = 7):
        """Remove data older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        keys_to_remove = []
        for key, game_data in self.game_data.items():
            try:
                game_date = datetime.strptime(game_data.date, '%Y-%m-%d')
                if game_date < cutoff_date:
                    keys_to_remove.append(key)
            except:
                continue
        
        for key in keys_to_remove:
            del self.game_data[key]
        
        if keys_to_remove:
            print(f"🧹 Cleaned up {len(keys_to_remove)} old game records")
            self.save_data()

# Global instance
cumulative_manager = CumulativeSimulationManager()

def test_cumulative_system():
    """Test the cumulative simulation system"""
    print("🧪 Testing Cumulative Simulation System")
    print("=" * 50)
    
    # Simulate some data
    test_results = [
        {"away_score": 4, "home_score": 7},
        {"away_score": 2, "home_score": 3},
        {"away_score": 6, "home_score": 4},
        {"away_score": 1, "home_score": 8},
        {"away_score": 5, "home_score": 2}
    ]
    
    # Add first batch
    print("Adding first batch of 5 simulations...")
    game_data = cumulative_manager.add_simulation_batch(
        "Yankees", "Red Sox", "2025-08-09", test_results
    )
    
    print(f"After batch 1: {game_data.total_simulations} total simulations")
    print(f"Home win probability: {game_data.home_win_probability:.1%}")
    
    # Add second batch
    print("\nAdding second batch of 5 simulations...")
    game_data = cumulative_manager.add_simulation_batch(
        "Yankees", "Red Sox", "2025-08-09", test_results
    )
    
    print(f"After batch 2: {game_data.total_simulations} total simulations")
    print(f"Home win probability: {game_data.home_win_probability:.1%}")
    print(f"Confidence level: {game_data.confidence_level:.1f}%")
    
    # Check if more simulations needed
    needs_more, count = cumulative_manager.should_run_more_simulations(
        "Yankees", "Red Sox", "2025-08-09", target_simulations=20
    )
    print(f"\nNeeds more simulations: {needs_more}")
    if needs_more:
        print(f"Recommended batch size: {count}")
    
    # Summary
    summary = cumulative_manager.get_simulation_summary()
    print(f"\n📊 Summary:")
    print(f"Total games: {summary['total_games']}")
    print(f"Total simulations: {summary['total_simulations']}")
    print(f"Average per game: {summary['average_sims_per_game']:.0f}")

if __name__ == "__main__":
    test_cumulative_system()
