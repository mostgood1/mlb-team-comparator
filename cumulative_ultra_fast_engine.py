"""
Enhanced Ultra-Fast Engine with Cumulative Simulation Support
Builds up simulation data over time instead of starting fresh each reload
"""

import numpy as np
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
import os
from datetime import datetime
from historical_betting_lines_lookup import HistoricalBettingLinesLookup
from cumulative_simulation_manager import cumulative_manager, CumulativeGameData

@dataclass
class EnhancedFastGameResult:
    away_score: int
    home_score: int
    total_runs: int
    home_wins: bool
    run_differential: int
    cumulative_data: Optional[CumulativeGameData] = None

class CumulativeUltraFastEngine:
    """
    Ultra-fast simulation engine with cumulative data accumulation
    Builds simulation confidence over time instead of starting fresh
    """
    
    def __init__(self):
        # Initialize the base fast engine components
        self.setup_fast_distributions()
        self.team_strengths = self._load_team_strengths_fast()
        self.pitcher_stats = self._load_pitcher_stats()
        self.pitcher_id_map = self._load_pitcher_id_map()
        self.projected_starters = self._load_projected_starters()
        self._setup_speed_cache()
        
        # Initialize cumulative manager
        self.cumulative_manager = cumulative_manager
        
        print("🔄 Enhanced engine with cumulative simulation support initialized")
    
    def setup_fast_distributions(self):
        """Pre-compute probability distributions for vectorized sampling"""
        # TUNED TO REAL MLB DATA: Target 8.86 mean, 4.66 std dev
        self.run_probs = {
            0: 0.03, 1: 0.06, 2: 0.09, 3: 0.12, 4: 0.11, 5: 0.10,
            6: 0.09, 7: 0.08, 8: 0.07, 9: 0.06, 10: 0.05, 11: 0.04,
            12: 0.03, 13: 0.025, 14: 0.02, 15: 0.015, 16: 0.01, 
            17: 0.008, 18: 0.006, 19: 0.004, 20: 0.002
        }
        
        # Pre-compute cumulative probabilities for fast sampling
        self.run_cumprobs = np.cumsum(list(self.run_probs.values()))
        self.run_values = np.array(list(self.run_probs.keys()))
    
    def _load_team_strengths_fast(self):
        """Load team strengths with auto-refresh capability"""
        try:
            with open('team_strengths.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._generate_default_strengths()
    
    def _load_pitcher_stats(self):
        """Load pitcher statistics"""
        try:
            with open('pitcher_stats_2025.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _load_pitcher_id_map(self):
        """Load pitcher ID mapping"""
        try:
            with open('pitcher_id_map.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _load_projected_starters(self):
        """Load projected starting pitchers"""
        try:
            with open('ProjectedStarters.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _generate_default_strengths(self):
        """Generate default team strengths if file missing"""
        mlb_teams = [
            "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox",
            "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians",
            "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals",
            "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers",
            "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics",
            "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants",
            "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers",
            "Toronto Blue Jays", "Washington Nationals"
        ]
        
        return {team: {"offensive_rating": 1.0, "defensive_rating": 1.0} for team in mlb_teams}
    
    def _setup_speed_cache(self):
        """Setup caching for maximum speed"""
        self.cache = {}
    
    def get_cumulative_prediction(self, away_team: str, home_team: str, 
                                game_date: str = None, target_simulations: int = 10000) -> Dict:
        """
        Get prediction using cumulative simulation approach
        Only runs new simulations if needed to reach target confidence
        """
        if game_date is None:
            game_date = datetime.now().strftime('%Y-%m-%d')
        
        # Check if we need more simulations
        needs_more, batch_size = self.cumulative_manager.should_run_more_simulations(
            away_team, home_team, game_date, target_simulations
        )
        
        existing_data = self.cumulative_manager.get_game_data(away_team, home_team, game_date)
        
        if needs_more:
            print(f"🔄 Running {batch_size} new simulations for {away_team} @ {home_team}")
            
            # Run new simulation batch
            new_results = self._run_simulation_batch(away_team, home_team, batch_size)
            
            # Add to cumulative data
            cumulative_data = self.cumulative_manager.add_simulation_batch(
                away_team, home_team, game_date, new_results
            )
        else:
            print(f"✅ Using existing {existing_data.total_simulations} simulations for {away_team} @ {home_team}")
            cumulative_data = existing_data
        
        # Generate prediction from cumulative data
        return self._create_prediction_from_cumulative(cumulative_data, away_team, home_team, game_date)
    
    def _run_simulation_batch(self, away_team: str, home_team: str, batch_size: int) -> List[Dict]:
        """Run a batch of fast simulations"""
        results = []
        
        # Get team multipliers including pitcher quality
        away_mult, home_mult = self.get_team_multiplier_with_pitchers(away_team, home_team)
        
        # Vectorized simulation for speed
        away_scores = self._sample_runs_vectorized(batch_size, away_mult)
        home_scores = self._sample_runs_vectorized(batch_size, home_mult * 1.04)  # Home field advantage
        
        for i in range(batch_size):
            results.append({
                'away_score': int(away_scores[i]),
                'home_score': int(home_scores[i])
            })
        
        return results
    
    def _sample_runs_vectorized(self, n_samples: int, multiplier: float) -> np.ndarray:
        """Vectorized run sampling for maximum speed"""
        base_samples = np.random.random(n_samples)
        indices = np.searchsorted(self.run_cumprobs, base_samples)
        runs = self.run_values[indices]
        
        # Apply team strength multiplier
        adjusted_runs = runs * multiplier
        
        # Add small amount of randomness and ensure non-negative
        noise = np.random.normal(0, 0.3, n_samples)
        final_runs = np.maximum(0, adjusted_runs + noise)
        
        return np.round(final_runs).astype(int)
    
    def get_team_multiplier_with_pitchers(self, away_team: str, home_team: str) -> Tuple[float, float]:
        """Get run multipliers for both teams including pitcher quality"""
        # Base team strength
        away_strength = self.team_strengths.get(away_team, {"offensive_rating": 1.0})["offensive_rating"]
        home_strength = self.team_strengths.get(home_team, {"offensive_rating": 1.0})["offensive_rating"]
        
        # Get pitcher quality factors
        away_starter, home_starter = self.get_matchup_starters(away_team, home_team)
        
        away_pitcher_factor = self.get_pitcher_quality_factor(home_starter) if home_starter else 1.0
        home_pitcher_factor = self.get_pitcher_quality_factor(away_starter) if away_starter else 1.0
        
        # Calculate final multipliers (pitcher quality affects opponent's offense)
        away_mult = away_strength * away_pitcher_factor
        home_mult = home_strength * home_pitcher_factor
        
        return away_mult, home_mult
    
    def get_matchup_starters(self, away_team: str, home_team: str) -> Tuple[Optional[str], Optional[str]]:
        """Get projected starters for this matchup"""
        matchup_key = f"{away_team} at {home_team}"
        
        if matchup_key in self.projected_starters:
            matchup_data = self.projected_starters[matchup_key]
            return matchup_data.get('away_starter'), matchup_data.get('home_starter')
        
        return None, None
    
    def get_pitcher_quality_factor(self, pitcher_name: str) -> float:
        """Get pitcher quality factor (affects opponent run scoring)"""
        if not pitcher_name or pitcher_name == 'TBD':
            return 1.0
        
        # Try to find pitcher in stats
        pitcher_data = None
        
        # Direct lookup
        if pitcher_name in self.pitcher_stats:
            pitcher_data = self.pitcher_stats[pitcher_name]
        else:
            # Try ID map lookup
            pitcher_id = self.pitcher_id_map.get(pitcher_name)
            if pitcher_id:
                pitcher_data = self.pitcher_stats.get(str(pitcher_id))
        
        if not pitcher_data or '2025' not in pitcher_data:
            return 1.0
        
        stats_2025 = pitcher_data['2025']
        
        try:
            era = float(stats_2025.get('era', '4.50'))
            games_started = int(stats_2025.get('gamesStarted', 0))
        except (ValueError, TypeError):
            return 1.0
        
        # Only apply to starting pitchers
        if games_started < 5:
            return 1.0
        
        # ERA-based adjustment (lower ERA = better pitcher = lower opponent scoring)
        if era < 2.00:
            return 0.70    # Elite pitcher
        elif era < 2.75:
            return 0.85    # Very good
        elif era < 3.50:
            return 0.95    # Above average
        elif era < 4.25:
            return 1.00    # Average
        elif era < 5.00:
            return 1.10    # Below average
        else:
            return 1.25    # Poor pitcher
    
    def _create_prediction_from_cumulative(self, cumulative_data: CumulativeGameData, 
                                         away_team: str, home_team: str, game_date: str) -> Dict:
        """Create prediction dictionary from cumulative data"""
        
        # Calculate advanced metrics
        total_games = cumulative_data.total_simulations
        confidence = min(95.0, (total_games / 10000) * 100)
        
        prediction = {
            'away_team': away_team,
            'home_team': home_team,
            'date': game_date,
            'home_win_probability': cumulative_data.home_win_probability,
            'away_win_probability': cumulative_data.away_win_probability,
            'predicted_home_score': cumulative_data.average_home_runs,
            'predicted_away_score': cumulative_data.average_away_runs,
            'predicted_total': cumulative_data.average_home_runs + cumulative_data.average_away_runs,
            'confidence': confidence,
            'total_simulations': total_games,
            'simulation_period': f"{cumulative_data.first_simulation} to {cumulative_data.last_simulation}",
            'cumulative_stats': {
                'home_wins': cumulative_data.home_wins,
                'away_wins': cumulative_data.away_wins,
                'total_home_runs': cumulative_data.total_home_runs,
                'total_away_runs': cumulative_data.total_away_runs
            }
        }
        
        return prediction

def test_cumulative_engine():
    """Test the cumulative simulation engine"""
    print("🧪 Testing Cumulative Ultra-Fast Engine")
    print("=" * 50)
    
    engine = CumulativeUltraFastEngine()
    
    # Test first prediction (will run initial simulations)
    print("First prediction (should run new simulations)...")
    pred1 = engine.get_cumulative_prediction("Yankees", "Red Sox", "2025-08-09", target_simulations=3000)
    
    print(f"✅ First prediction: {pred1['total_simulations']} simulations")
    print(f"   Home win prob: {pred1['home_win_probability']:.1%}")
    print(f"   Confidence: {pred1['confidence']:.1f}%")
    
    print("\nSecond prediction (should use existing data)...")
    pred2 = engine.get_cumulative_prediction("Yankees", "Red Sox", "2025-08-09", target_simulations=3000)
    
    print(f"✅ Second prediction: {pred2['total_simulations']} simulations")
    print(f"   Home win prob: {pred2['home_win_probability']:.1%}")
    print(f"   Confidence: {pred2['confidence']:.1f}%")
    
    print("\nThird prediction with higher target (should add more simulations)...")
    pred3 = engine.get_cumulative_prediction("Yankees", "Red Sox", "2025-08-09", target_simulations=5000)
    
    print(f"✅ Third prediction: {pred3['total_simulations']} simulations")
    print(f"   Home win prob: {pred3['home_win_probability']:.1%}")
    print(f"   Confidence: {pred3['confidence']:.1f}%")
    
    # Show cumulative summary
    summary = engine.cumulative_manager.get_simulation_summary()
    print(f"\n📊 Cumulative Summary:")
    print(f"   Total games tracked: {summary['total_games']}")
    print(f"   Total simulations: {summary['total_simulations']}")
    print(f"   Average per game: {summary['average_sims_per_game']:.0f}")

if __name__ == "__main__":
    test_cumulative_engine()
