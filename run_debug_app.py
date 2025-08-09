"""
Quick test to see if the issue is with data or frontend
"""
from app import app

# Add a simple debug route
@app.route('/debug-games')
def debug_games():
    """Simple debug route to check if games are available"""
    try:
        from ultra_fast_engine import FastPredictionEngine
        engine = FastPredictionEngine()
        
        import TodaysGames
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        games = TodaysGames.get_games_for_date(today)
        
        html = f"""
        <h1>🔧 Debug Games Data</h1>
        <p><strong>Date:</strong> {today}</p>
        <p><strong>Games Found:</strong> {len(games)}</p>
        <h2>Games List:</h2>
        <ul>
        """
        
        for i, game in enumerate(games[:10]):
            away = game.get('away_team', 'Unknown')
            home = game.get('home_team', 'Unknown')
            html += f"<li>{i+1}. {away} @ {home}</li>"
            
        html += """
        </ul>
        <h2>Test Prediction:</h2>
        """
        
        if games:
            first_game = games[0]
            away_team = first_game.get('away_team', 'Unknown')
            home_team = first_game.get('home_team', 'Unknown')
            
            try:
                prediction = engine.get_fast_prediction(away_team, home_team)
                html += f"""
                <p><strong>Test Game:</strong> {away_team} @ {home_team}</p>
                <p><strong>Predicted Total:</strong> {prediction.get('predictions', {}).get('predicted_total_runs', 'N/A')}</p>
                <p><strong>Execution Time:</strong> {prediction.get('meta', {}).get('execution_time_ms', 'N/A')}ms</p>
                """
            except Exception as e:
                html += f"<p><strong>Prediction Error:</strong> {e}</p>"
        
        html += """
        <br><br>
        <a href="/">← Back to Main Interface</a>
        """
        
        return html
        
    except Exception as e:
        return f"<h1>❌ Debug Error</h1><p>{e}</p><a href='/'>← Back</a>"

if __name__ == '__main__':
    print("🚀 Starting app with debug route...")
    print("📝 Visit http://localhost:5000/debug-games to check data")
    print("📝 Visit http://localhost:5000/ for main interface")
    app.run(host='localhost', port=5000, debug=True)
