# ⚡ Ultra-Fast MLB Predictions - Complete Minimal Deployment

A streamlined version of the MLB prediction system focused solely on ultra-fast web predictions with full betting analysis.

## Features

- **Sub-200ms Predictions**: Vectorized simulations for real-time performance
- **Smart Betting Analysis**: Kelly criterion sizing with expected value calculations  
- **Real Betting Lines**: Historical and current betting line integration
- **Team Strength Modeling**: Advanced team performance factors
- **Realistic Variance**: Tuned to 2,548 real MLB games
- **Pitcher Quality Integration**: Advanced pitcher performance modeling
- **Real-time Web Interface**: Interactive dashboard with live predictions

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web server:
```bash
python app.py
```

3. Open browser to http://localhost:5000

## Complete File Set

**Core Engine:**
- `ultra_fast_engine.py` - Main prediction engine with vectorized simulations
- `app.py` - Flask web interface with real-time predictions

**Essential Data:**
- `pitcher_stats_2025_and_career.json` - Pitcher quality factors (1.25MB)
- `ProjectedStarters.json` - Daily matchup data
- `pitcher_id_map.json` - Player ID mappings
- `mlb_betting_lines.json` - Current betting lines  
- `historical_betting_lines_cache.json` - Historical betting data
- `team_strength_cache.json` - Team performance factors

**Supporting Modules:**
- `historical_betting_lines_lookup.py` - Historical line lookups
- `TodaysGames.py` - Real game schedule integration

## Performance

- **Target**: <200ms per prediction ✅
- **Simulations**: 1,500-3,000 per prediction
- **Throughput**: 20,000+ simulations per second  
- **Memory**: <100MB total
- **Repository Size**: 1.34MB (GitHub friendly)

## API Endpoints

- `/` - Main web interface
- `/api/fast-predictions` - Get multiple predictions for today's games
- `/api/speed-test` - Performance benchmarking
- `/api/debug-pitcher` - Pitcher data debugging
- `/api/scenario-analysis` - Multi-scenario analysis
- `/api/status` - System status

## Betting Analysis

- **Expected Value Calculations**: Proper probability vs payout analysis
- **Kelly Criterion Sizing**: Optimal bet sizing recommendations
- **Edge Detection**: Model vs market probability comparison
- **Real Line Integration**: Uses actual betting lines when available
- **Historical Lookups**: Past game line reconstruction

## Complete System

This minimal deployment includes ALL essential files for the ultra-fast MLB prediction system:
✅ Betting lines and historical data  
✅ Team strength modeling  
✅ Pitcher quality integration  
✅ Real game schedule integration  
✅ Web interface with full features  
✅ GitHub deployment ready (<2MB total)
