"""
Ultra-Fast MLB Prediction Web Interface
Real-time betting recommendations with sub-200ms prediction generation
Updated to use REAL GAME          <div         <div class="header">
            <h1>⚡ Ultra-Fast MLB Predictions</h1>
            <p>💰 DAILY BETTING RECOMMENDATIONS: Professional analysis for today's games • Real-time value detection • Historical accuracy validation</p>
        </div>
        
        <div class="speed-banner">
            📈 ACCURACY REVIEW MODE: Select any date to see predicted vs actual results and track model performance!
        </div>
                        if (pred.betting_lines) {
                            // Moneyline analysis
                            const mlFavorite = pred.betting_lines.moneyline_favorite;
                            const predictedWinner = (pred.predictions.away_score > pred.predictions.home_score) ? pred.away_team : pred.home_team;
                            const actualWinner = (pred.actual_results.away_score > pred.actual_results.home_score) ? pred.away_team : pred.home_team;
                            
                            if (mlFavorite) {
                                totalMoneyline++;
                                if (predictedWinner === actualWinner) moneylineCorrect++;
                            }
                            
                            // Over/Under analysis
                            if (pred.betting_lines.total_line) {
                                totalOverUnder++;
                                const totalLine = pred.betting_lines.total_line;
                                const predictedOU = predictedTotal > totalLine ? 'Over' : 'Under';
                                const actualOU = actualTotal > totalLine ? 'Over' : 'Under';
                                if (predictedOU === actualOU) overUnderCorrect++;
                            }
                        }
                    }
                });
                
                const winnerAccuracy = totalGames > 0 ? (winnersCorrect / totalGames * 100).toFixed(1) : 'N/A';
                const avgTotalError = totalRunsErrors.length > 0 ? (totalRunsErrors.reduce((a,b) => a+b, 0) / totalRunsErrors.length).toFixed(1) : 'N/A';
                const goodTotalPredictions = totalRunsErrors.filter(err => err <= 2).length;
                const totalAccuracy = totalRunsErrors.length > 0 ? (goodTotalPredictions / totalRunsErrors.length * 100).toFixed(1) : 'N/A';
                const overUnderAccuracy = totalOverUnder > 0 ? (overUnderCorrect / totalOverUnder * 100).toFixed(1) : 'N/A';
                const moneylineAccuracy = totalMoneyline > 0 ? (moneylineCorrect / totalMoneyline * 100).toFixed(1) : 'N/A';
                
                // Determine overall performance level
                const winnerPct = parseFloat(winnerAccuracy) || 0;
                const totalPct = parseFloat(totalAccuracy) || 0;
                const avgError = parseFloat(avgTotalError) || 0;
                
                let performanceLevel = '';
                let performanceColor = '';
                let performanceIcon = '';
                
                if (winnerPct >= 60 && totalPct >= 70 && avgError <= 1.5) {
                    performanceLevel = 'EXCELLENT';
                    performanceColor = '#28a745';
                    performanceIcon = '🏆';
                } else if (winnerPct >= 50 && totalPct >= 60 && avgError <= 2.0) {
                    performanceLevel = 'GOOD';
                    performanceColor = '#ffc107';
                    performanceIcon = '✅';
                } else if (winnerPct >= 40 && totalPct >= 50) {
                    performanceLevel = 'FAIR';
                    performanceColor = '#fd7e14';
                    performanceIcon = '📊';
                } else {
                    performanceLevel = 'NEEDS IMPROVEMENT';
                    performanceColor = '#dc3545';
                    performanceIcon = '⚠️';
                }
                
                headerDiv.style.backgroundColor = 'rgba(255, 193, 7, 0.2)';
                headerDiv.style.textAlign = 'center';
                headerDiv.innerHTML = `
                    <h2>📊 Model Accuracy Review - ${gameDate || 'Historical Date'}</h2>
                    <div style="background: rgba(${performanceColor === '#28a745' ? '40, 167, 69' : performanceColor === '#ffc107' ? '255, 193, 7' : performanceColor === '#fd7e14' ? '253, 126, 20' : '220, 53, 69'}, 0.2); padding: 12px; border-radius: 8px; margin: 10px 0; border-left: 4px solid ${performanceColor};">
                        <div style="font-size: 1.3em; font-weight: bold; color: ${performanceColor};">${performanceIcon} OVERALL PERFORMANCE: ${performanceLevel}</div>
                        <div style="font-size: 0.95em; margin-top: 5px; opacity: 0.9;">
                            Winner Accuracy: ${winnerAccuracy}% • Total Runs Accuracy: ${totalAccuracy}% • Avg Error: ${avgTotalError} runs • Games Analyzed: ${totalGames}
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 15px 0;">
                        <div style="background: rgba(40, 167, 69, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #28a745;">🎯 Winner Predictions</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${winnersCorrect}/${totalGames} (${winnerAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Model vs Actual Game Winners</div>
                        </div>
                        <div style="background: rgba(52, 152, 219, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #3498db;">📊 Total Runs Accuracy</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${goodTotalPredictions}/${totalRunsErrors.length} (${totalAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Within 2 runs • Avg Error: ${avgTotalError}</div>
                        </div>
                        <div style="background: rgba(255, 193, 7, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #e67e22;">💰 Over/Under vs Lines</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${overUnderCorrect}/${totalOverUnder} (${overUnderAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Model O/U vs Betting Lines</div>
                        </div>
                        <div style="background: rgba(156, 39, 176, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #9c27b0;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #9c27b0;">💸 Moneyline Performance</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${moneylineCorrect}/${totalMoneyline} (${moneylineAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Model picks vs ML Favorites</div>
                        </div>
                    </div>
                    
                    <div style="background: rgba(52, 73, 94, 0.3); padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <h3 style="color: #ecf0f1; margin-bottom: 10px;">📈 Performance Analysis</h3>
                        <p style="margin: 5px 0; font-size: 0.95em;"><strong>Model vs Betting Markets:</strong> How our predictions performed against professional oddsmakers</p>
                        <p style="margin: 5px 0; font-size: 0.95em;"><strong>Individual Game Breakdown:</strong> Each game shows Model Pick vs Betting Favorite vs Actual Result</p>
                    </div>
                `;
            } else {rDiv = document.createElement('div');
            headerDiv.className = 'prediction-card';
            if (isHistorical) {
                // Calculate overall accuracy stats for historical data
                let winnersCorrect = 0;
                let totalGames = 0;
                let totalRunsErrors = [];
                
                predictions.forEach(pred => {
                    if (pred.actual_results && pred.actual_results.winner_correct !== undefined) {
                        totalGames++;
                        if (pred.actual_results.winner_correct) winnersCorrect++;
                        
                        const actualTotal = (pred.actual_results.away_score || 0) + (pred.actual_results.home_score || 0);
                        const predictedTotal = pred.predictions.predicted_total_runs || (pred.predictions.away_score + pred.predictions.home_score) || 0;
                        const error = Math.abs(actualTotal - predictedTotal);
                        if (!isNaN(error)) totalRunsErrors.push(error);
                    }
                });
                
                const winnerAccuracy = totalGames > 0 ? (winnersCorrect / totalGames * 100).toFixed(1) : 'N/A';
                const avgTotalError = totalRunsErrors.length > 0 ? (totalRunsErrors.reduce((a,b) => a+b, 0) / totalRunsErrors.length).toFixed(1) : 'N/A';
                const goodTotalPredictions = totalRunsErrors.filter(err => err <= 2).length;
                const totalAccuracy = totalRunsErrors.length > 0 ? (goodTotalPredictions / totalRunsErrors.length * 100).toFixed(1) : 'N/A';
                
                // Determine overall performance level
                const winnerPct = parseFloat(winnerAccuracy) || 0;
                const totalPct = parseFloat(totalAccuracy) || 0;
                const avgError = parseFloat(avgTotalError) || 0;
                
                let performanceLevel = '';
                let performanceColor = '';
                let performanceIcon = '';
                
                if (winnerPct >= 60 && totalPct >= 70 && avgError <= 1.5) {
                    performanceLevel = 'EXCELLENT';
                    performanceColor = '#28a745';
                    performanceIcon = '🏆';
                } else if (winnerPct >= 50 && totalPct >= 60 && avgError <= 2.0) {
                    performanceLevel = 'GOOD';
                    performanceColor = '#ffc107';
                    performanceIcon = '✅';
                } else if (winnerPct >= 40 && totalPct >= 50) {
                    performanceLevel = 'FAIR';
                    performanceColor = '#fd7e14';
                    performanceIcon = '📊';
                } else {
                    performanceLevel = 'NEEDS IMPROVEMENT';
                    performanceColor = '#dc3545';
                    performanceIcon = '⚠️';
                }
                
                headerDiv.style.backgroundColor = 'rgba(255, 193, 7, 0.2)';
                headerDiv.style.textAlign = 'center';
                headerDiv.innerHTML = `
                    <h2>📊 Model Accuracy Review - ${gameDate || 'Historical Date'}</h2>
                    <div style="background: rgba(${performanceColor === '#28a745' ? '40, 167, 69' : performanceColor === '#ffc107' ? '255, 193, 7' : performanceColor === '#fd7e14' ? '253, 126, 20' : '220, 53, 69'}, 0.2); padding: 12px; border-radius: 8px; margin: 10px 0; border-left: 4px solid ${performanceColor};">
                        <div style="font-size: 1.3em; font-weight: bold; color: ${performanceColor};">${performanceIcon} OVERALL PERFORMANCE: ${performanceLevel}</div>
                        <div style="font-size: 0.95em; margin-top: 5px; opacity: 0.9;">
                            Winner Accuracy: ${winnerAccuracy}% • Total Runs Accuracy: ${totalAccuracy}% • Avg Error: ${avgTotalError} runs • Games Analyzed: ${totalGames}
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
                        <div style="background: rgba(40, 167, 69, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #28a745;">🎯 Winner Predictions</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${winnersCorrect}/${totalGames} (${winnerAccuracy}%)</div>
                        </div>
                        <div style="background: rgba(52, 152, 219, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #3498db;">📊 Total Runs Accuracy</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${goodTotalPredictions}/${totalRunsErrors.length} (${totalAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Avg Error: ${avgTotalError} runs</div>
                        </div>
                    </div>
                    <p>🎯 Final scores vs predictions • Individual game accuracy breakdown below</p>
                `;
            } else {
                headerDiv.style.backgroundColor = 'rgba(40, 167, 69, 0.2)';
                headerDiv.style.textAlign = 'center';
                headerDiv.innerHTML = `<h2>💰 ${gameDate ? gameDate : "Today's"} Betting Recommendations</h2>
                                      <p>⚡ Live predictions with professional betting analysis • Real pitcher matchups</p>`;
            }v class="header">
            <h1>⚡ Ultra-Fast MLB Predictions</h1>
            <p>💰 DAILY BETTING RECOMMENDATIONS: Professional analysis for today's games • Real-time value detection • Historical accuracy validation</p>
        </div>
        
        <div class="speed-banner">
            🎯 PRIMARY: Get today's betting recommendations • SECONDARY: Review historical accuracy with past game results
        </div>lass="header">
            <h1>⚡ Ultra-Fast MLB Predictions</h1>
            <p>💰 DAILY BETTING RECOMMENDATIONS: Professional analysis for today's games • Real-time value detection • Historical accuracy validation</p>
        </div>
        
        <div class="speed-banner">
            🎯 PRIMARY: Get today's betting recommendations • SECONDARY: Review historical accuracy with past game results
        </div>th actual pitcher matchups
"""

from flask import Flask, render_template_string, jsonify, request
import traceback
import json
import os
from datetime import datetime, date
from typing import Dict, List

# Load team assets for enhanced UI
try:
    team_assets_path = os.path.join(os.path.dirname(__file__), 'mlb_team_assets.json')
    with open(team_assets_path, 'r', encoding='utf-8') as f:
        TEAM_ASSETS = json.load(f)
    print("✓ MLB team assets loaded successfully")
    print(f"   Loaded {len(TEAM_ASSETS)} teams with logos and colors")
except Exception as e:
    print(f"⚠ Team assets not available: {e}")
    TEAM_ASSETS = {}

# Import the ultra-fast engine
try:
    from ultra_fast_engine import FastPredictionEngine
    print("✓ Ultra-fast engine imported successfully")
    ULTRA_FAST_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Ultra-fast engine not available: {e}")
    ULTRA_FAST_AVAILABLE = False

# Import betting lines auto-updater
try:
    from auto_update_betting_lines import BettingLinesAutoUpdater
    print("✓ Betting lines auto-updater imported successfully")
    BETTING_UPDATER_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Betting lines auto-updater not available: {e}")
    BETTING_UPDATER_AVAILABLE = False

# Fallback imports
try:
    from improved_prediction_engine import ImprovedMLBPredictionEngine
    print("✓ Improved engine available as fallback")
    IMPROVED_AVAILABLE = True
except ImportError:
    IMPROVED_AVAILABLE = False

# Import TodaysGames for real game data
try:
    from TodaysGames import TodaysGames
    print("✓ TodaysGames module imported successfully")
    TODAYS_GAMES_AVAILABLE = True
except ImportError as e:
    print(f"⚠ TodaysGames module not available: {e}")
    TODAYS_GAMES_AVAILABLE = False

app = Flask(__name__)

# Initialize betting lines auto-updater
def initialize_betting_lines():
    """Initialize and run betting lines auto-updater on startup"""
    if BETTING_UPDATER_AVAILABLE:
        try:
            print("🔄 Initializing betting lines auto-updater...")
            updater = BettingLinesAutoUpdater()
            
            # Check if betting lines need updating
            if updater.should_update_betting_lines(max_age_hours=3):
                print("📊 Updating betting lines on startup...")
                success = updater.update_betting_lines()
                if success:
                    print("✅ Betting lines updated successfully on startup")
                else:
                    print("⚠️ Betting lines update failed on startup")
            else:
                print("✅ Betting lines are current")
                
        except Exception as e:
            print(f"❌ Error initializing betting lines updater: {e}")
    else:
        print("⚠️ Betting lines auto-updater not available")

# Run betting lines initialization
initialize_betting_lines()

# Enhanced HTML template with real-time features
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Ultra-Fast MLB Predictions - REAL GAMES</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.8em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .speed-banner {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            padding: 15px; border-radius: 10px; margin-bottom: 20px;
            text-align: center; font-weight: bold; font-size: 1.2em;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.8; } }
        
        .prediction-card {
            background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
            border-radius: 15px; padding: 25px; margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .matchup { text-align: center; font-size: 1.5em; margin-bottom: 20px; font-weight: bold; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; }
        .stat-box { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center; }
        .stat-label { font-size: 0.9em; opacity: 0.8; margin-bottom: 5px; }
        .stat-value { font-size: 1.3em; font-weight: bold; }
        .performance-stats { 
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; 
            margin-bottom: 20px; font-size: 0.9em;
        }
        .perf-box { background: rgba(52, 152, 219, 0.2); padding: 8px; border-radius: 8px; text-align: center; }
        
        .recommendations-section { margin-top: 25px; }
        .rec-header { font-size: 1.3em; margin-bottom: 15px; font-weight: bold; }
        .recommendation {
            background: linear-gradient(45deg, rgba(46, 204, 113, 0.3), rgba(39, 174, 96, 0.3));
            padding: 15px; border-radius: 12px; margin-bottom: 10px;
            border-left: 4px solid #2ecc71;
        }
        .rec-type { font-size: 1.1em; font-weight: bold; margin-bottom: 8px; }
        .rec-details { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; }
        .rec-stat { font-size: 0.9em; }
        .rec-reasoning { margin-top: 10px; font-style: italic; opacity: 0.9; }
        
        .no-recs {
            background: rgba(108, 117, 125, 0.2); padding: 15px; border-radius: 12px;
            text-align: center; opacity: 0.8;
        }
        
        .controls { text-align: center; margin-bottom: 20px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; }
        button { 
            background: linear-gradient(45deg, #3498db, #2980b9); color: white; border: none;
            padding: 12px 24px; border-radius: 25px; font-size: 1em; cursor: pointer;
            transition: all 0.3s; min-width: 150px;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .loading { text-align: center; font-size: 1.2em; margin: 20px 0; }
        
        .speed-indicator {
            position: fixed; top: 10px; right: 10px; 
            background: linear-gradient(45deg, #e74c3c, #c0392b);
            padding: 8px 15px; border-radius: 20px; font-size: 0.9em; font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .execution-time {
            background: rgba(231, 76, 60, 0.2); padding: 10px; border-radius: 8px;
            text-align: center; margin-bottom: 15px; font-weight: bold;
        }
        
        .pitcher-summary {
            margin-top: 10px; padding: 15px; 
            background: rgba(255, 193, 7, 0.2); 
            border-radius: 8px; font-size: 0.95em;
            border-left: 3px solid #ffc107;
        }
        
        .pitcher-factor {
            font-weight: bold; 
            color: #ffc107;
        }
        
        .real-game-badge {
            background: linear-gradient(45deg, #28a745, #20c997);
            padding: 5px 12px; border-radius: 15px; font-size: 0.85em;
            margin-left: 10px; display: inline-block; color: white;
            font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="speed-indicator">⚡ REAL GAMES</div>
    
    <div class="container">
        <div class="header">
            <h1>⚡ Ultra-Fast MLB Predictions</h1>
            <p>🎯 MODEL ACCURACY TRACKER: Review prediction performance across historical dates • Validate system accuracy</p>
        </div>
        
        <div class="speed-banner">
            � ACCURACY REVIEW MODE: Select any date to see predicted vs actual results and track model performance!
        </div>
        
        <div class="controls">
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 15px;">
                <button onclick="loadTodaysRealGames()" style="background: linear-gradient(45deg, #28a745, #20c997); font-size: 1.1em; padding: 15px 25px;">💰 Today's Betting Recommendations</button>
                <button onclick="speedTest()">⚡ Speed Test</button>
                <button onclick="showMultipleGames()">📊 Game Analysis</button>
            </div>
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; align-items: center;">
                <span style="color: #ecf0f1; font-weight: bold;">📈 Historical Accuracy Review:</span>
                <input type="date" id="game-date" style="padding: 8px; border-radius: 6px; border: 1px solid #ddd; font-size: 0.9em;" />
                <button onclick="loadGamesForDate()" style="background: linear-gradient(45deg, #6c757d, #5a6268); font-size: 0.9em;">� Review Accuracy</button>
            </div>
        </div>
        
        <div id="predictions-container"></div>
    </div>

    <script>
        let currentEngine = null;
        
        // Team assets cache
        let teamAssets = {};
        
        // Load team assets on page load
        async function loadTeamAssets() {
            try {
                const response = await fetch('/api/team-assets');
                teamAssets = await response.json();
                console.log('✓ Team assets loaded:', Object.keys(teamAssets).length, 'teams');
                
                // Log first few teams for debugging
                const firstTeams = Object.keys(teamAssets).slice(0, 3);
                firstTeams.forEach(team => {
                    console.log(`${team}: ${teamAssets[team].logo_emoji} ${teamAssets[team].primary_color}`);
                });
                
                return true;
            } catch (error) {
                console.warn('⚠ Could not load team assets:', error);
                return false;
            }
        }
        
        // Get team assets for a team with better fallback
        function getTeamAssets(teamName) {
            if (!teamName) {
                return {
                    primary_color: '#2c3e50',
                    secondary_color: '#ecf0f1',
                    logo_emoji: '⚾',
                    short_name: 'Team'
                };
            }
            
            // Special cases for team name variations (engine uses short names)
            const teamMappings = {
                'Royals': 'Kansas City Royals',
                'Twins': 'Minnesota Twins', 
                'Athletics': 'Oakland Athletics',
                'Angels': 'Los Angeles Angels',
                'Astros': 'Houston Astros',
                'Mariners': 'Seattle Mariners',
                'Orioles': 'Baltimore Orioles',
                'Rangers': 'Texas Rangers',
                'Rays': 'Tampa Bay Rays',
                'Red Sox': 'Boston Red Sox',
                'Tigers': 'Detroit Tigers',
                'White Sox': 'Chicago White Sox',
                'Yankees': 'New York Yankees',
                'Blue Jays': 'Toronto Blue Jays',
                'Guardians': 'Cleveland Guardians',
                'Braves': 'Atlanta Braves',
                'Brewers': 'Milwaukee Brewers',
                'Cardinals': 'St. Louis Cardinals',
                'Cubs': 'Chicago Cubs',
                'Diamondbacks': 'Arizona Diamondbacks',
                'Dodgers': 'Los Angeles Dodgers',
                'Giants': 'San Francisco Giants',
                'Marlins': 'Miami Marlins',
                'Mets': 'New York Mets',
                'Nationals': 'Washington Nationals',
                'Padres': 'San Diego Padres',
                'Phillies': 'Philadelphia Phillies',
                'Pirates': 'Pittsburgh Pirates',
                'Reds': 'Cincinnati Reds',
                'Rockies': 'Colorado Rockies'
            };
            
            // Check team mappings FIRST (most common case)
            if (teamMappings[teamName] && teamAssets[teamMappings[teamName]]) {
                console.log(`🎯 Mapped "${teamName}" -> "${teamMappings[teamName]}"`);
                return teamAssets[teamMappings[teamName]];
            }
            
            // Try exact match second
            if (teamAssets[teamName]) {
                console.log(`🎯 Direct match for "${teamName}"`);
                return teamAssets[teamName];
            }
            
            // Try to find by short name or partial match
            for (const [fullName, assets] of Object.entries(teamAssets)) {
                if (assets.short_name === teamName || 
                    fullName.includes(teamName) || 
                    teamName.includes(assets.short_name)) {
                    console.log(`🎯 Partial match "${teamName}" -> "${fullName}"`);
                    return assets;
                }
            }
            
            // Return default if not found
            console.warn(`Team assets not found for: ${teamName}`);
            return {
                primary_color: '#2c3e50',
                secondary_color: '#ecf0f1',
                logo_emoji: '⚾',
                short_name: teamName || 'Team'
            };
        }
        
        // Create team-styled HTML elements
        function createTeamStyledElement(teamName, content, elementType = 'div') {
            const assets = getTeamAssets(teamName);
            return `<${elementType} style="
                background: linear-gradient(135deg, ${assets.primary_color}15, ${assets.secondary_color}15);
                border-left: 4px solid ${assets.primary_color};
                color: ${assets.primary_color};
                font-weight: bold;
            ">${assets.logo_emoji} ${content}</${elementType}>`;
        }
        
        // Create team logo span with debugging
        function createTeamLogo(teamName) {
            console.log(`🎨 Creating logo for: "${teamName}"`);
            const assets = getTeamAssets(teamName);
            console.log(`🎨 Assets found:`, assets);
            
            const logoHtml = `<span style="
                background: linear-gradient(135deg, ${assets.primary_color}, ${assets.secondary_color}30);
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                display: inline-block;
                margin: 0 5px;
            ">${assets.logo_emoji} ${assets.short_name || teamName}</span>`;
            
            console.log(`🎨 Generated HTML:`, logoHtml);
            return logoHtml;
        }

        // Load team assets when page loads and ensure they're available
        document.addEventListener('DOMContentLoaded', async () => {
            console.log('🎨 Loading team assets...');
            await loadTeamAssets();
            console.log('✅ Page initialization complete');
        });
        
        async function loadTodaysRealGames() {
            document.getElementById('predictions-container').innerHTML = '<div class="loading">⚡ Loading today\\'s REAL games with actual pitcher matchups...</div>';
            
            // Ensure team assets are loaded
            if (Object.keys(teamAssets).length === 0) {
                console.log('🎨 Team assets not loaded, loading now...');
                await loadTeamAssets();
            }
            
            try {
                const response = await fetch('/api/real-games-predictions');
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                const data = await response.json();
                
                if (data.error) throw new Error(data.error);
                
                if (!data.predictions || data.predictions.length === 0) {
                    throw new Error('No predictions returned from server');
                }
                
                displayMultiplePredictions(data.predictions);
            } catch (error) {
                console.error('loadTodaysRealGames error:', error);
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card">
                        <h3>❌ No Live Games Available Today</h3>
                        <p><strong>Error:</strong> ${error.message}</p>
                        <p><strong>Suggestion:</strong> Use the date selector above to review historical model accuracy. Start with August 8, 2025 which has complete game results.</p>
                        <div style="margin-top: 15px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                            <button onclick="document.getElementById('game-date').value='2025-08-08'; loadGamesForDate();" 
                                    style="margin-top: 10px; padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 4px; font-weight: bold;">
                                � Review Aug 8 Accuracy
                            </button>
                        </div>
                    </div>`;
            }
        }
        
        async function loadGamesForDate() {
            const selectedDate = document.getElementById('game-date').value;
            if (!selectedDate) {
                alert('Please select a date first');
                return;
            }
            
            // Ensure team assets are loaded
            if (Object.keys(teamAssets).length === 0) {
                console.log('🎨 Team assets not loaded, loading now...');
                await loadTeamAssets();
            }
            
            document.getElementById('predictions-container').innerHTML = `<div class="loading">⚡ Loading games for ${selectedDate}...</div>`;
            
            try {
                const response = await fetch(`/api/games-predictions?date=${selectedDate}`);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                const data = await response.json();
                
                if (data.error) throw new Error(data.error);
                
                if (!data.predictions || data.predictions.length === 0) {
                    throw new Error(`No games found for ${selectedDate}`);
                }
                
                displayMultiplePredictions(data.predictions, selectedDate);
            } catch (error) {
                console.error('loadGamesForDate error:', error);
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card">
                        <h3>❌ No Accuracy Data Available for ${selectedDate}</h3>
                        <p><strong>Error:</strong> ${error.message}</p>
                        <p><strong>Available dates:</strong> August 8, 2025 currently has complete historical accuracy data. More dates will be added as the system tracks performance over time.</p>
                        <button onclick="document.getElementById('game-date').value='2025-08-08'; loadGamesForDate();" 
                                style="margin-top: 10px; padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 4px;">
                            � Review Aug 8 Accuracy
                        </button>
                    </div>`;
            }
        }
        
        async function speedTest() {
            document.getElementById('predictions-container').innerHTML = '<div class="loading">⚡ Running speed test with real games...</div>';
            
            try {
                const response = await fetch('/api/speed-test');
                const data = await response.json();
                
                let html = `
                    <div class="prediction-card">
                        <h3>⚡ Speed Test Results (Real Games)</h3>
                        <div class="stats-grid">
                            <div class="stat-box">
                                <div class="stat-label">Average Time</div>
                                <div class="stat-value">${data.average_time_ms}ms</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Fastest</div>
                                <div class="stat-value">${data.fastest_ms}ms</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Total Simulations</div>
                                <div class="stat-value">${data.total_simulations}</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Sims per Second</div>
                                <div class="stat-value">${data.sims_per_second}</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px; padding: 15px; background: rgba(46, 204, 113, 0.2); border-radius: 8px;">
                            <strong>Performance Analysis:</strong><br>
                            ${data.performance_note}
                        </div>
                    </div>
                `;
                
                document.getElementById('predictions-container').innerHTML = html;
            } catch (error) {
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card"><h3>❌ Error: ${error.message}</h3></div>`;
            }
        }
        
        async function showMultipleGames() {
            document.getElementById('predictions-container').innerHTML = '<div class="loading">📊 Analyzing today\\'s real games...</div>';
            
            try {
                const response = await fetch('/api/real-games-predictions');
                const data = await response.json();
                
                if (data.error) throw new Error(data.error);
                
                const predictions = data.predictions;
                const totalScores = predictions.map(p => p.predictions.predicted_total_runs);
                const avgTotal = totalScores.reduce((a,b) => a+b, 0) / totalScores.length;
                const minTotal = Math.min(...totalScores);
                const maxTotal = Math.max(...totalScores);
                
                const highScoring = predictions.filter(p => p.predictions.predicted_total_runs >= 10);
                const lowScoring = predictions.filter(p => p.predictions.predicted_total_runs <= 6);
                const closeGames = predictions.filter(p => Math.abs(p.predictions.predicted_away_score - p.predictions.predicted_home_score) <= 1);
                
                let html = `
                    <div class="prediction-card">
                        <h3>📊 Real Games Analysis Dashboard</h3>
                        <div style="background: rgba(46, 204, 113, 0.15); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                            <h4 style="color: #2ecc71; margin-bottom: 10px;">🎯 REAL GAME DATA ACTIVE</h4>
                            <p>Using actual pitcher matchups • Verified impact factors • Today's live MLB games</p>
                        </div>
                        
                        <div class="stats-grid">
                            <div class="stat-box">
                                <div class="stat-label">Average Total</div>
                                <div class="stat-value">${avgTotal.toFixed(1)} runs</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Range</div>
                                <div class="stat-value">${minTotal.toFixed(1)} - ${maxTotal.toFixed(1)}</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">High-Scoring</div>
                                <div class="stat-value">${highScoring.length} games</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Close Games</div>
                                <div class="stat-value">${closeGames.length} games</div>
                            </div>
                        </div>
                        
                        <div style="background: rgba(52, 152, 219, 0.15); padding: 15px; border-radius: 8px; margin-top: 20px;">
                            <h4 style="color: #3498db; margin-bottom: 10px;">⚡ Performance Metrics</h4>
                            <div class="performance-stats">
                                <div class="perf-box">
                                    <strong>Total Time</strong><br>${data.total_time_ms.toFixed(1)}ms
                                </div>
                                <div class="perf-box">
                                    <strong>Avg per Game</strong><br>${(data.total_time_ms / data.predictions.length).toFixed(1)}ms
                                </div>
                                <div class="perf-box">
                                    <strong>Predictions/Sec</strong><br>${(data.predictions.length / (data.total_time_ms/1000)).toFixed(1)}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                document.getElementById('predictions-container').innerHTML = html;
                
                setTimeout(() => {
                    document.getElementById('predictions-container').innerHTML += `
                        <div style="text-align: center; margin-top: 20px;">
                            <button onclick="showDetailedResults()" 
                                    style="background: linear-gradient(45deg, #28a745, #20c997); padding: 12px 24px;">
                                📋 View Individual Game Details
                            </button>
                        </div>
                    `;
                }, 100);
                
            } catch (error) {
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card"><h3>❌ Error: ${error.message}</h3></div>`;
            }
        }
        
        async function testRecommendations() {
            document.getElementById('predictions-container').innerHTML = '<div class="loading">💰 Testing betting recommendations with real games...</div>';
            
            try {
                const response = await fetch('/api/real-games-predictions');
                const data = await response.json();
                
                if (data.error) throw new Error(data.error);
                
                const gamesWithRecs = data.predictions.filter(pred => pred.recommendations && pred.recommendations.length > 0);
                
                let html = `
                    <div class="prediction-card">
                        <h3>💰 Real Game Betting Analysis</h3>
                        <div style="background: rgba(255, 193, 7, 0.15); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                            <h4 style="color: #ffc107; margin-bottom: 10px;">🎯 Live Value Detection</h4>
                            <p>Real pitcher matchups • Verified impact factors • Professional betting analysis</p>
                        </div>
                        
                        <div class="stats-grid">
                            <div class="stat-box">
                                <div class="stat-label">Games Analyzed</div>
                                <div class="stat-value">${data.predictions.length}</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Value Found</div>
                                <div class="stat-value">${gamesWithRecs.length}</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">Value Rate</div>
                                <div class="stat-value">${(gamesWithRecs.length / data.predictions.length * 100).toFixed(1)}%</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label">System Status</div>
                                <div class="stat-value">LIVE</div>
                            </div>
                        </div>
                        
                        ${gamesWithRecs.length > 0 ? `
                            <div style="margin-top: 20px; padding: 15px; background: rgba(46, 204, 113, 0.15); border-radius: 8px;">
                                <strong>✅ Value opportunities found in real games!</strong> Professional betting recommendations available.
                            </div>
                        ` : `
                            <div style="margin-top: 20px; padding: 15px; background: rgba(108, 117, 125, 0.2); border-radius: 8px;">
                                No high-value betting opportunities found in today's real games. System monitoring continues.
                            </div>
                        `}
                    </div>
                `;
                
                document.getElementById('predictions-container').innerHTML = html;
                
            } catch (error) {
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card"><h3>❌ Error: ${error.message}</h3></div>`;
            }
        }
        
        function createHistoricalPredictionHTML(data) {
            const pred = data.predictions;
            const actual = data.actual_results;
            const meta = data.meta;
            
            // Calculate accuracy indicators with safe fallbacks
            const predictedTotal = pred.predicted_total_runs || (pred.away_score + pred.home_score) || 0;
            const actualTotal = (actual.away_score + actual.home_score) || 0;
            const scoreDiff = Math.abs((pred.away_score + pred.home_score) - actualTotal);
            const winnerCorrect = actual.winner_correct;
            const totalError = Math.abs(predictedTotal - actualTotal);
            
            return `
                <div class="execution-time" style="background: rgba(255, 193, 7, 0.2);">
                    � Historical Accuracy Data - ${meta.matched_key || 'Cached Result'}
                </div>
                
                <div class="matchup">
                    ${createTeamLogo(data.away_team)} @ ${createTeamLogo(data.home_team)}
                    <span class="real-game-badge" style="background: linear-gradient(45deg, #ffc107, #e0a800);">ACCURACY REVIEW</span>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Predicted Score</div>
                        <div class="stat-value">${pred.away_score.toFixed(1)} - ${pred.home_score.toFixed(1)}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Actual Score</div>
                        <div class="stat-value" style="color: #28a745; font-weight: bold;">${actual.away_score} - ${actual.home_score}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Winner Accuracy</div>
                        <div class="stat-value" style="color: ${winnerCorrect ? '#28a745' : '#dc3545'};">
                            ${winnerCorrect ? '✅ CORRECT' : '❌ WRONG'}
                        </div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Total Runs Error</div>
                        <div class="stat-value" style="color: ${totalError <= 2 ? '#28a745' : totalError <= 4 ? '#ffc107' : '#dc3545'};">
                            ${totalError.toFixed(1)} runs off
                        </div>
                    </div>
                </div>
                
                <div class="pitcher-summary">
                    <strong>⚾ Starting Pitchers (Final Matchup):</strong><br>
                    <span class="pitcher-factor">Away:</span> ${actual.away_pitcher || data.away_pitcher || meta.away_pitcher || 'Not Available'}<br>
                    <span class="pitcher-factor">Home:</span> ${actual.home_pitcher || data.home_pitcher || meta.home_pitcher || 'Not Available'}
                    ${(actual.away_pitcher && actual.home_pitcher) ? '' : '<br><small style="opacity: 0.7;">📝 Pitcher data may not be available for this historical game</small>'}
                </div>
                
                <div style="margin-top: 15px; padding: 15px; background: rgba(255, 193, 7, 0.1); border-radius: 8px; border-left: 3px solid #ffc107;">
                    <h4 style="color: #e67e22; margin-bottom: 10px;">💸 Betting Lines vs Model Performance</h4>
                    <div style="margin: 10px 0; padding: 12px; background: rgba(156, 39, 176, 0.2); border-radius: 8px; border-left: 3px solid #9c27b0;">
                        <strong>🎯 Moneyline Analysis:</strong><br>
                        • Betting Favorite: ${data.betting_lines?.moneyline_favorite || 'Not Available'}<br>
                        • Model Predicted: ${(pred.away_score > pred.home_score) ? data.away_team : data.home_team}<br>
                        • Actual Winner: ${(actual.away_score > actual.home_score) ? data.away_team : data.home_team}<br>
                        • Model vs Favorite: <span style="color: ${((pred.away_score > pred.home_score) ? data.away_team : data.home_team) === (data.betting_lines?.moneyline_favorite || '') ? '#28a745' : '#f39c12'}; font-weight: bold;">${((pred.away_score > pred.home_score) ? data.away_team : data.home_team) === (data.betting_lines?.moneyline_favorite || '') ? 'AGREED' : 'DISAGREED'}</span><br>
                        • Model Accuracy: <span style="color: ${winnerCorrect ? '#28a745' : '#dc3545'}; font-weight: bold;">${winnerCorrect ? '✅ CORRECT' : '❌ WRONG'}</span>
                    </div>
                    ${data.betting_lines?.total_line ? `
                        <div style="margin: 10px 0; padding: 12px; background: rgba(52, 152, 219, 0.2); border-radius: 8px; border-left: 3px solid #3498db;">
                            <strong>💰 Over/Under Analysis (Line: ${data.betting_lines.total_line}):</strong><br>
                            • Model Predicted: ${predictedTotal > data.betting_lines.total_line ? 'Over' : 'Under'} (${predictedTotal.toFixed(1)} runs)<br>
                            • Actual Result: ${actualTotal > data.betting_lines.total_line ? 'Over' : 'Under'} (${actualTotal} runs)<br>
                            • Model O/U Accuracy: <span style="color: ${(predictedTotal > data.betting_lines.total_line) === (actualTotal > data.betting_lines.total_line) ? '#28a745' : '#dc3545'}; font-weight: bold;">${(predictedTotal > data.betting_lines.total_line) === (actualTotal > data.betting_lines.total_line) ? '✅ CORRECT' : '❌ WRONG'}</span>
                        </div>
                    ` : ''}
                </div>
                
                <div style="margin-top: 15px; padding: 10px; background: rgba(40, 167, 69, 0.1); border-radius: 8px; border-left: 3px solid #28a745;">
                    <strong>📊 Accuracy Summary:</strong><br>
                    • Predicted Total: ${predictedTotal.toFixed(1)} runs | Actual: ${actualTotal} runs<br>
                    • Winner Prediction: ${(pred.away_score > pred.home_score) ? data.away_team : data.home_team} | Actual Winner: ${(actual.away_score > actual.home_score) ? data.away_team : data.home_team}<br>
                    • Prediction Error: ${totalError.toFixed(1)} runs
                </div>
            `;
        }
        
        function createPredictionHTML(data, isHistorical = false) {
            if (isHistorical && data.result_type === 'HISTORICAL') {
                return createHistoricalPredictionHTML(data);
            }
            
            const p = data.predictions;
            const meta = data.meta;
            const recs = data.recommendations;
            const pitchers = data.pitcher_quality || {};
            
            // Get team assets for styling
            const awayAssets = getTeamAssets(data.away_team);
            const homeAssets = getTeamAssets(data.home_team);
            
            let html = `
                <div class="execution-time">
                    ⚡ Generated in ${meta.execution_time_ms}ms with ${meta.simulations_run} simulations
                </div>
                
                <div class="matchup" style="
                    background: linear-gradient(135deg, ${awayAssets.primary_color}20, ${homeAssets.primary_color}20);
                    border-radius: 12px;
                    padding: 15px;
                    margin: 15px 0;
                ">
                    ${createTeamLogo(data.away_team)} @ ${createTeamLogo(data.home_team)}
                    <span class="real-game-badge">REAL GAME</span>
                </div>
                
                <div class="performance-stats">
                    <div class="perf-box">
                        <strong>Speed</strong><br>${meta.execution_time_ms}ms
                    </div>
                    <div class="perf-box">
                        <strong>Confidence</strong><br>${p.confidence}%
                    </div>
                    <div class="perf-box">
                        <strong>Recommendations</strong><br>${meta.recommendations_found}
                    </div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Win Probability</div>
                        <div class="stat-value">${createTeamLogo(data.away_team)} ${(p.away_win_prob * 100).toFixed(1)}% | ${createTeamLogo(data.home_team)} ${(p.home_win_prob * 100).toFixed(1)}%</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Predicted Score</div>
                        <div class="stat-value">${p.predicted_away_score} - ${p.predicted_home_score}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Total Runs</div>
                        <div class="stat-value">${p.predicted_total_runs}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Range</div>
                        <div class="stat-value">${p.total_runs_range[0]} - ${p.total_runs_range[1]}</div>
                    </div>
                </div>
                
                <!-- Betting Odds Display -->
                ${data.betting_lines ? `
                <div style="margin: 15px 0; padding: 15px; background: rgba(255, 193, 7, 0.1); border-radius: 8px; border-left: 3px solid #ffc107;">
                    <h4 style="color: #e67e22; margin-bottom: 10px; font-size: 1.1em;">💸 Current Betting Lines</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        ${data.betting_lines.home_ml && data.betting_lines.away_ml ? `
                        <div style="padding: 10px; background: rgba(156, 39, 176, 0.2); border-radius: 6px;">
                            <div style="font-weight: bold; color: #9c27b0; margin-bottom: 5px;">🎯 Moneyline</div>
                            <div style="font-size: 0.9em;">
                                ${createTeamLogo(data.away_team)}: ${data.betting_lines.away_ml}<br>
                                ${createTeamLogo(data.home_team)}: ${data.betting_lines.home_ml}<br>
                                <strong>Favorite: ${createTeamLogo(data.betting_lines.away_ml < data.betting_lines.home_ml ? data.away_team : data.home_team)}</strong>
                            </div>
                        </div>
                        ` : ''}
                        ${data.betting_lines.total_line ? `
                        <div style="padding: 10px; background: rgba(52, 152, 219, 0.2); border-radius: 6px;">
                            <div style="font-weight: bold; color: #3498db; margin-bottom: 5px;">💰 Over/Under</div>
                            <div style="font-size: 0.9em;">
                                Total: <strong>${data.betting_lines.total_line}</strong><br>
                                Over: ${data.betting_lines.over_odds || '-110'}<br>
                                Under: ${data.betting_lines.under_odds || '-110'}
                            </div>
                        </div>
                        ` : ''}
                    </div>
                    ${data.betting_lines.spread_home ? `
                    <div style="margin-top: 10px; padding: 10px; background: rgba(40, 167, 69, 0.2); border-radius: 6px;">
                        <div style="font-weight: bold; color: #28a745; margin-bottom: 5px;">📊 Run Line (1.5)</div>
                        <div style="font-size: 0.9em; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div>${createTeamLogo(data.away_team)} ${data.betting_lines.spread_home > 0 ? '+1.5' : '-1.5'}: ${data.betting_lines.spread_odds || '-110'}</div>
                            <div>${createTeamLogo(data.home_team)} ${data.betting_lines.spread_home < 0 ? '+1.5' : '-1.5'}: ${data.betting_lines.spread_odds || '-110'}</div>
                        </div>
                    </div>
                    ` : ''}
                </div>
                ` : `
                <div style="margin: 15px 0; padding: 15px; background: rgba(108, 117, 125, 0.1); border-radius: 8px; border-left: 3px solid #6c757d;">
                    <h4 style="color: #6c757d; margin-bottom: 5px; font-size: 1.1em;">💸 Betting Lines</h4>
                    <div style="font-size: 0.9em; color: #6c757d;">Betting lines not available for this game</div>
                </div>
                `}
                
                <div class="pitcher-summary">
                    <strong>⚾ Starting Pitchers (Real Matchup):</strong><br>
                    <div style="margin: 8px 0;">${createTeamStyledElement(data.away_team, `${pitchers.away_pitcher_name || 'TBD'} (Impact: ${(pitchers.away_pitcher_factor || 1.0).toFixed(3)})`, 'div')}</div>
                    <div style="margin: 8px 0;">${createTeamStyledElement(data.home_team, `${pitchers.home_pitcher_name || 'TBD'} (Impact: ${(pitchers.home_pitcher_factor || 1.0).toFixed(3)})`, 'div')}</div>
                    <div style="margin-top: 8px; font-size: 0.9em; opacity: 0.9;">
                        💡 Impact Factor: &lt;1.0 = reduces runs allowed, &gt;1.0 = allows more runs
                    </div>
                </div>
                
                <div class="recommendations-section">
                    <div class="rec-header">💰 Betting Recommendations</div>
            `;
            
            if (recs && recs.length > 0) {
                recs.forEach(rec => {
                    html += `
                        <div class="recommendation">
                            <div class="rec-type">
                                🔥 ${rec.type.toUpperCase()}: ${rec.side.toUpperCase()}
                                ${rec.confidence === 'HIGH' ? '🚀' : '📈'}
                            </div>
                            <div class="rec-details">
                                <div class="rec-stat"><strong>EV:</strong> ${(rec.expected_value * 100).toFixed(1)}%</div>
                                <div class="rec-stat"><strong>Edge:</strong> ${(rec.edge * 100).toFixed(1)}%</div>
                                <div class="rec-stat"><strong>Kelly:</strong> ${rec.kelly_bet_size}%</div>
                                <div class="rec-stat"><strong>Odds:</strong> ${rec.odds}</div>
                            </div>
                            <div class="rec-reasoning">${rec.reasoning}</div>
                        </div>
                    `;
                });
            } else {
                html += '<div class="no-recs">No betting value identified at current lines</div>';
            }
            
            html += `</div>`;
            return html;
        }

        function displayMultiplePredictions(predictions, gameDate = null) {
            const container = document.getElementById('predictions-container');
            container.innerHTML = '';
            
            // Determine if this is historical data
            const isHistorical = predictions.length > 0 && predictions[0].result_type === 'HISTORICAL';
            
            // Add header with comprehensive accuracy analysis for historical data
            const headerDiv = document.createElement('div');
            headerDiv.className = 'prediction-card';
            if (isHistorical) {
                // Calculate overall accuracy stats for historical data
                let winnersCorrect = 0;
                let totalGames = 0;
                let totalRunsErrors = [];
                let overUnderCorrect = 0;
                let moneylineCorrect = 0;
                let totalOverUnder = 0;
                let totalMoneyline = 0;
                
                predictions.forEach(pred => {
                    if (pred.actual_results && pred.actual_results.winner_correct !== undefined) {
                        totalGames++;
                        if (pred.actual_results.winner_correct) winnersCorrect++;
                        
                        const actualTotal = (pred.actual_results.away_score || 0) + (pred.actual_results.home_score || 0);
                        const predictedTotal = pred.predictions.predicted_total_runs || (pred.predictions.away_score + pred.predictions.home_score) || 0;
                        const error = Math.abs(actualTotal - predictedTotal);
                        if (!isNaN(error)) totalRunsErrors.push(error);
                        
                        // Check if betting line data is available
                        if (pred.betting_lines) {
                            // Moneyline analysis
                            const mlFavorite = pred.betting_lines.moneyline_favorite;
                            const predictedWinner = (pred.predictions.away_score > pred.predictions.home_score) ? pred.away_team : pred.home_team;
                            const actualWinner = (pred.actual_results.away_score > pred.actual_results.home_score) ? pred.away_team : pred.home_team;
                            
                            if (mlFavorite) {
                                totalMoneyline++;
                                if (predictedWinner === actualWinner) moneylineCorrect++;
                            }
                            
                            // Over/Under analysis
                            if (pred.betting_lines.total_line) {
                                totalOverUnder++;
                                const totalLine = pred.betting_lines.total_line;
                                const predictedOU = predictedTotal > totalLine ? 'Over' : 'Under';
                                const actualOU = actualTotal > totalLine ? 'Over' : 'Under';
                                if (predictedOU === actualOU) overUnderCorrect++;
                            }
                        }
                    }
                });
                
                const winnerAccuracy = totalGames > 0 ? (winnersCorrect / totalGames * 100).toFixed(1) : 'N/A';
                const avgTotalError = totalRunsErrors.length > 0 ? (totalRunsErrors.reduce((a,b) => a+b, 0) / totalRunsErrors.length).toFixed(1) : 'N/A';
                const goodTotalPredictions = totalRunsErrors.filter(err => err <= 2).length;
                const totalAccuracy = totalRunsErrors.length > 0 ? (goodTotalPredictions / totalRunsErrors.length * 100).toFixed(1) : 'N/A';
                const overUnderAccuracy = totalOverUnder > 0 ? (overUnderCorrect / totalOverUnder * 100).toFixed(1) : 'N/A';
                const moneylineAccuracy = totalMoneyline > 0 ? (moneylineCorrect / totalMoneyline * 100).toFixed(1) : 'N/A';
                
                // Determine overall performance level
                const winnerPct = parseFloat(winnerAccuracy) || 0;
                const totalPct = parseFloat(totalAccuracy) || 0;
                const avgError = parseFloat(avgTotalError) || 0;
                
                let performanceLevel = '';
                let performanceColor = '';
                let performanceIcon = '';
                
                if (winnerPct >= 60 && totalPct >= 70 && avgError <= 1.5) {
                    performanceLevel = 'EXCELLENT';
                    performanceColor = '#28a745';
                    performanceIcon = '🏆';
                } else if (winnerPct >= 50 && totalPct >= 60 && avgError <= 2.0) {
                    performanceLevel = 'GOOD';
                    performanceColor = '#ffc107';
                    performanceIcon = '✅';
                } else if (winnerPct >= 40 && totalPct >= 50) {
                    performanceLevel = 'FAIR';
                    performanceColor = '#fd7e14';
                    performanceIcon = '📊';
                } else {
                    performanceLevel = 'NEEDS IMPROVEMENT';
                    performanceColor = '#dc3545';
                    performanceIcon = '⚠️';
                }
                
                headerDiv.style.backgroundColor = 'rgba(255, 193, 7, 0.2)';
                headerDiv.style.textAlign = 'center';
                headerDiv.innerHTML = `
                    <h2>📊 Model Accuracy Review - ${gameDate || 'Historical Date'}</h2>
                    <div style="background: rgba(${performanceColor === '#28a745' ? '40, 167, 69' : performanceColor === '#ffc107' ? '255, 193, 7' : performanceColor === '#fd7e14' ? '253, 126, 20' : '220, 53, 69'}, 0.2); padding: 12px; border-radius: 8px; margin: 10px 0; border-left: 4px solid ${performanceColor};">
                        <div style="font-size: 1.3em; font-weight: bold; color: ${performanceColor};">${performanceIcon} OVERALL PERFORMANCE: ${performanceLevel}</div>
                        <div style="font-size: 0.95em; margin-top: 5px; opacity: 0.9;">
                            Winner Accuracy: ${winnerAccuracy}% • Total Runs Accuracy: ${totalAccuracy}% • Avg Error: ${avgTotalError} runs • Games Analyzed: ${totalGames}
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 15px 0;">
                        <div style="background: rgba(40, 167, 69, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #28a745;">🎯 Winner Predictions</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${winnersCorrect}/${totalGames} (${winnerAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Model vs Actual Game Winners</div>
                        </div>
                        <div style="background: rgba(52, 152, 219, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #3498db;">📊 Total Runs Accuracy</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${goodTotalPredictions}/${totalRunsErrors.length} (${totalAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Within 2 runs • Avg Error: ${avgTotalError}</div>
                        </div>
                        <div style="background: rgba(255, 193, 7, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #e67e22;">💰 Over/Under vs Lines</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${overUnderCorrect}/${totalOverUnder} (${overUnderAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Model O/U vs Betting Lines</div>
                        </div>
                        <div style="background: rgba(156, 39, 176, 0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #9c27b0;">
                            <div style="font-size: 1.1em; font-weight: bold; color: #9c27b0;">💸 Moneyline Performance</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${moneylineCorrect}/${totalMoneyline} (${moneylineAccuracy}%)</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">Model picks vs ML Favorites</div>
                        </div>
                    </div>
                    
                    <div style="background: rgba(52, 73, 94, 0.3); padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <h3 style="color: #ecf0f1; margin-bottom: 10px;">📈 Performance Analysis</h3>
                        <p style="margin: 5px 0; font-size: 0.95em;"><strong>Model vs Betting Markets:</strong> How our predictions performed against professional oddsmakers</p>
                        <p style="margin: 5px 0; font-size: 0.95em;"><strong>Individual Game Breakdown:</strong> Each game shows Model Pick vs Betting Favorite vs Actual Result</p>
                    </div>
                `;
            } else {
                headerDiv.style.backgroundColor = 'rgba(40, 167, 69, 0.2)';
                headerDiv.style.textAlign = 'center';
                headerDiv.innerHTML = `<h2>💰 ${gameDate ? gameDate : "Today's"} Betting Recommendations</h2>
                                      <p>⚡ Live predictions with professional betting analysis • Real pitcher matchups</p>`;
            }
            container.appendChild(headerDiv);
            
            predictions.forEach(pred => {
                const predictionDiv = document.createElement('div');
                predictionDiv.className = 'prediction-card';
                
                // Apply team-specific border styling
                const awayAssets = getTeamAssets(pred.away_team);
                const homeAssets = getTeamAssets(pred.home_team);
                predictionDiv.style.borderImage = `linear-gradient(45deg, ${awayAssets.primary_color}, ${homeAssets.primary_color}) 1`;
                predictionDiv.style.borderWidth = '2px';
                predictionDiv.style.borderStyle = 'solid';
                predictionDiv.style.background = `linear-gradient(135deg, rgba(255,255,255,0.1), ${awayAssets.primary_color}05, ${homeAssets.primary_color}05)`;
                
                predictionDiv.innerHTML = createPredictionHTML(pred, isHistorical);
                container.appendChild(predictionDiv);
            });
        }
        
        function showDetailedResults() {
            // This function will reload the current games with detailed view
            const dateInput = document.getElementById('game-date');
            if (dateInput && dateInput.value) {
                loadGamesForDate();
            } else {
                loadTodaysRealGames();
            }
        }
        
        function loadHistoricalDemo() {
            // Legacy function - redirect to date-based accuracy review
            document.getElementById('game-date').value = '2025-08-08';
            loadGamesForDate();
        }
        
        // Auto-load today's betting recommendations on page load
        window.onload = () => {
            // Set today's date in the date picker for easy historical access
            const today = new Date();
            const todayStr = today.toISOString().split('T')[0];
            document.getElementById('game-date').value = todayStr;
            
            // Load today's betting recommendations as primary purpose
            loadTodaysRealGames();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page with ultra-fast prediction interface using real games"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/real-games-predictions')
def get_real_games_predictions():
    """Get predictions for today's real games with actual pitcher matchups"""
    try:
        if ULTRA_FAST_AVAILABLE:
            engine = FastPredictionEngine()
            
            # Get today's real games
            real_games = engine.get_todays_real_games()
            
            if not real_games:
                # If no games today, try August 8, 2025 (our complete historical date)
                real_games = engine.get_todays_real_games("2025-08-08")
                games_source = 'Historical games (Aug 8, 2025) - No games available for today'
            else:
                games_source = 'ProjectedStarters.json - Real MLB games'
            
            predictions = []
            start_time = datetime.now()
            
            for away, home in real_games:
                prediction = engine.get_fast_prediction(away, home, sim_count=1500)
                predictions.append(prediction)
            
            total_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return jsonify({
                'success': True,
                'predictions': predictions,
                'total_time_ms': total_time,
                'total_games': len(real_games),
                'games_source': games_source
            })
        else:
            return jsonify({'error': 'Ultra-fast engine not available'})
            
    except Exception as e:
        return jsonify({'error': f'Error generating real game predictions: {str(e)}'})

@app.route('/api/games-predictions')
def get_games_predictions():
    """Get predictions for games on a specific date (supports historical data)"""
    try:
        game_date = request.args.get('date')
        if not game_date:
            return jsonify({'error': 'Date parameter is required'})
            
        if ULTRA_FAST_AVAILABLE:
            engine = FastPredictionEngine()
            
            # Get games for the specified date
            real_games = engine.get_todays_real_games(game_date)
            
            if not real_games:
                return jsonify({
                    'error': f'No accuracy data available for {game_date}. Model performance tracking starts with August 8, 2025.',
                    'suggestion': 'August 8, 2025 has complete accuracy validation data with 15 games showing predicted vs actual results.'
                })
            
            predictions = []
            start_time = datetime.now()
            
            for away, home in real_games:
                # Pass the game_date to enable historical lookup
                prediction = engine.get_fast_prediction(away, home, sim_count=1500, game_date=game_date)
                predictions.append(prediction)
            
            total_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Check if any predictions are historical
            historical_count = sum(1 for p in predictions if p.get('result_type') == 'HISTORICAL')
            
            return jsonify({
                'success': True,
                'predictions': predictions,
                'total_time_ms': total_time,
                'total_games': len(real_games),
                'historical_games': historical_count,
                'live_games': len(real_games) - historical_count,
                'game_date': game_date,
                'games_source': f'Accuracy data for {game_date} - {"Model performance validation" if historical_count > 0 else "Live prediction tracking"}'
            })
        else:
            return jsonify({'error': 'Ultra-fast engine not available'})
            
    except Exception as e:
        return jsonify({'error': f'Error generating predictions for {game_date}: {str(e)}'})

@app.route('/api/speed-test')
def speed_test():
    """Test speed performance with real games"""
    try:
        if ULTRA_FAST_AVAILABLE:
            engine = FastPredictionEngine()
            real_games = engine.get_todays_real_games()
            
            times = []
            total_sims = 0
            
            # Run predictions on first 3 real games for speed test
            for i, (away, home) in enumerate(real_games[:3]):
                prediction = engine.get_fast_prediction(away, home, sim_count=2000)
                times.append(prediction['meta']['execution_time_ms'])
                total_sims += prediction['meta']['simulations_run']
            
            avg_time = sum(times) / len(times)
            fastest = min(times)
            sims_per_second = int(total_sims / (sum(times) / 1000))
            
            if avg_time < 100:
                performance_note = "🚀 EXCELLENT: Ultra-fast performance with real games!"
            elif avg_time < 200:
                performance_note = "✅ GOOD: Fast performance with real pitcher data"
            else:
                performance_note = "⚠️ SLOW: Performance below target with real games"
            
            return jsonify({
                'average_time_ms': round(avg_time, 1),
                'fastest_ms': round(fastest, 1),
                'total_simulations': total_sims,
                'sims_per_second': sims_per_second,
                'performance_note': performance_note,
                'individual_times': times,
                'games_tested': len(times)
            })
        else:
            return jsonify({'error': 'Ultra-fast engine not available'})
            
    except Exception as e:
        return jsonify({'error': f'Error in speed test: {str(e)}'})

@app.route('/api/team-assets')
def get_team_assets():
    """Get team assets for enhanced UI"""
    return jsonify(TEAM_ASSETS)

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        'ultra_fast_available': ULTRA_FAST_AVAILABLE,
        'real_games_active': True,
        'pitcher_impacts_active': True,
        'features': [
            'Real MLB game data',
            'Verified pitcher matchups',
            'Realistic impact factors', 
            'Sub-200ms predictions',
            'Professional betting analysis'
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/update-betting-lines')
def update_betting_lines():
    """Manually trigger betting lines update"""
    try:
        if BETTING_UPDATER_AVAILABLE:
            updater = BettingLinesAutoUpdater()
            print("🔄 Manual betting lines update requested...")
            
            # Force update regardless of age
            success = updater.update_betting_lines()
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Betting lines updated successfully',
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Betting lines update failed',
                    'timestamp': datetime.now().isoformat()
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Betting lines auto-updater not available',
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating betting lines: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    print("⚡ Starting Ultra-Fast MLB Prediction Web Interface")
    print(f"   Ultra-Fast Engine: {'✓ Available' if ULTRA_FAST_AVAILABLE else '❌ Not Available'}")
    print(f"   Real Game Data: ✓ Active")
    print(f"   Pitcher Impacts: ✓ Active") 
    print(f"   Starting server on http://localhost:5006")
    
    app.run(debug=True, host='0.0.0.0', port=5006)
