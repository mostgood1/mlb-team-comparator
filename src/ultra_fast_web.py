"""
Ultra-Fast MLB Prediction Web Interface
Real-time betting recommendations with sub-200ms prediction generation
Updated to use REAL GAME DATA with actual pitcher matchups
"""

from flask import Flask, render_template_string, jsonify, request
import traceback
from datetime import datetime, date
from typing import Dict, List

# Import the ultra-fast engine
try:
    from ultra_fast_engine import FastPredictionEngine
    print("✓ Ultra-fast engine imported successfully")
    ULTRA_FAST_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Ultra-fast engine not available: {e}")
    ULTRA_FAST_AVAILABLE = False

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
            <p>🎯 REAL GAME DATA: Actual pitcher matchups • Realistic impact factors • Live updated games</p>
        </div>
        
        <div class="speed-banner">
            🚀 NOW USING REAL GAMES: Today's actual MLB matchups with verified pitcher impacts!
        </div>
        
        <div class="controls">
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 15px;">
                <input type="date" id="game-date" style="padding: 12px; border-radius: 8px; border: 1px solid #ddd; font-size: 1em;" value="2025-08-08" />
                <button onclick="loadGamesForDate()">📅 Load Games for Date</button>
            </div>
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                <button onclick="loadTodaysRealGames()">🏟️ Today's Real Games</button>
                <button onclick="speedTest()">⚡ Speed Test</button>
                <button onclick="showMultipleGames()">📊 Detailed Analysis</button>
                <button onclick="testRecommendations()">💰 Test Recommendations</button>
            </div>
        </div>
        
        <div id="predictions-container"></div>
    </div>

    <script>
        let currentEngine = null;
        
        async function loadTodaysRealGames() {
            document.getElementById('predictions-container').innerHTML = '<div class="loading">⚡ Loading today\\'s REAL games with actual pitcher matchups...</div>';
            
            try {
                const response = await fetch('/api/real-games-predictions');
                const data = await response.json();
                
                if (data.error) throw new Error(data.error);
                displayMultiplePredictions(data.predictions);
            } catch (error) {
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card"><h3>❌ Error: ${error.message}</h3></div>`;
            }
        }
        
        async function loadGamesForDate() {
            const selectedDate = document.getElementById('game-date').value;
            if (!selectedDate) {
                alert('Please select a date first');
                return;
            }
            
            document.getElementById('predictions-container').innerHTML = `<div class="loading">⚡ Loading games for ${selectedDate}...</div>`;
            
            try {
                const response = await fetch(`/api/games-predictions?date=${selectedDate}`);
                const data = await response.json();
                
                if (data.error) throw new Error(data.error);
                displayMultiplePredictions(data.predictions, selectedDate);
            } catch (error) {
                document.getElementById('predictions-container').innerHTML = 
                    `<div class="prediction-card"><h3>❌ Error: ${error.message}</h3></div>`;
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
                            <button onclick="displayMultiplePredictions(${JSON.stringify(predictions).replace(/"/g, '&quot;')})" 
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
            
            // Calculate accuracy indicators
            const scoreDiff = Math.abs((pred.away_score + pred.home_score) - (actual.away_score + actual.home_score));
            const winnerCorrect = actual.winner_correct;
            
            return `
                <div class="execution-time" style="background: rgba(255, 193, 7, 0.2);">
                    🔒 Historical Data - Cached Prediction (${meta.matched_key})
                </div>
                
                <div class="matchup">
                    ✈️ ${data.away_team} @ 🏠 ${data.home_team}
                    <span class="real-game-badge" style="background: linear-gradient(45deg, #ffc107, #e0a800);">HISTORICAL</span>
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
                        <div class="stat-label">Prediction Error</div>
                        <div class="stat-value">${actual.prediction_error || scoreDiff.toFixed(1)} runs</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Winner Prediction</div>
                        <div class="stat-value" style="color: ${winnerCorrect ? '#28a745' : '#dc3545'};">
                            ${winnerCorrect ? '✅ Correct' : '❌ Incorrect'}
                        </div>
                    </div>
                </div>
                
                <div class="pitcher-summary">
                    <strong>⚾ Starting Pitchers (Historical Matchup):</strong><br>
                    <span class="pitcher-factor">Away:</span> ${actual.away_pitcher || 'Unknown'}<br>
                    <span class="pitcher-factor">Home:</span> ${actual.home_pitcher || 'Unknown'}
                </div>
                
                <div style="margin-top: 15px; padding: 10px; background: rgba(40, 167, 69, 0.1); border-radius: 8px; border-left: 3px solid #28a745;">
                    <strong>🎯 Accuracy Demonstration:</strong> This historical game shows how our prediction engine performed against the actual MLB result.
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
            
            let html = `
                <div class="execution-time">
                    ⚡ Generated in ${meta.execution_time_ms}ms with ${meta.simulations_run} simulations
                </div>
                
                <div class="matchup">
                    ✈️ ${data.away_team} @ 🏠 ${data.home_team}
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
                        <div class="stat-value">🏠 ${(p.home_win_prob * 100).toFixed(1)}% | ✈️ ${(p.away_win_prob * 100).toFixed(1)}%</div>
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
                
                <div class="pitcher-summary">
                    <strong>⚾ Starting Pitchers (Real Matchup):</strong><br>
                    <span class="pitcher-factor">Away:</span> ${pitchers.away_pitcher_name || 'TBD'} 
                    (Impact: <span class="pitcher-factor">${(pitchers.away_pitcher_factor || 1.0).toFixed(3)}</span>)<br>
                    <span class="pitcher-factor">Home:</span> ${pitchers.home_pitcher_name || 'TBD'} 
                    (Impact: <span class="pitcher-factor">${(pitchers.home_pitcher_factor || 1.0).toFixed(3)}</span>)
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
            
            // Add header
            const headerDiv = document.createElement('div');
            headerDiv.className = 'prediction-card';
            if (isHistorical) {
                headerDiv.style.backgroundColor = 'rgba(255, 193, 7, 0.2)';
                headerDiv.style.textAlign = 'center';
                headerDiv.innerHTML = `<h2>📚 Historical Games - ${gameDate || 'Past Date'}</h2>
                                      <p>🎯 Showing cached predictions with actual results for accuracy demonstration</p>`;
            } else {
                headerDiv.style.backgroundColor = 'rgba(40, 167, 69, 0.2)';
                headerDiv.style.textAlign = 'center';
                headerDiv.innerHTML = `<h2>🏟️ ${gameDate ? gameDate : "Today's"} Real MLB Games with Verified Pitcher Impacts</h2>`;
            }
            container.appendChild(headerDiv);
            
            predictions.forEach(pred => {
                const predictionDiv = document.createElement('div');
                predictionDiv.className = 'prediction-card';
                predictionDiv.innerHTML = createPredictionHTML(pred, isHistorical);
                container.appendChild(predictionDiv);
            });
        }
        
        // Auto-load today's real games on page load
        window.onload = () => {
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
                'games_source': 'ProjectedStarters.json - Real MLB games'
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
                'games_source': f'Games for {game_date} - {"Historical cache" if historical_count > 0 else "Live simulation"}'
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

if __name__ == '__main__':
    print("⚡ Starting Ultra-Fast MLB Prediction Web Interface")
    print(f"   Ultra-Fast Engine: {'✓ Available' if ULTRA_FAST_AVAILABLE else '❌ Not Available'}")
    print(f"   Real Game Data: ✓ Active")
    print(f"   Pitcher Impacts: ✓ Active") 
    print(f"   Starting server on http://localhost:5006")
    
    app.run(debug=True, host='0.0.0.0', port=5006)
