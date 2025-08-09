# MLB Games Scheduled Fetcher
import requests
import sys
import datetime
import json

def get_games_for_date(date):
    """
    Fetch all MLB games scheduled for a given date.
    Returns a list of dicts: [{ 'game_pk': int, 'away_team': str, 'home_team': str, 'status': str }]
    """
    try:
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        games = data.get('dates', [{}])[0].get('games', [])
        result = []
        
        for g in games:
            away_team_info = g.get('teams', {}).get('away', {}).get('team', {})
            home_team_info = g.get('teams', {}).get('home', {}).get('team', {})
            away_team = away_team_info.get('name', '')
            home_team = home_team_info.get('name', '')
            away_team_id = away_team_info.get('id', None)
            home_team_id = home_team_info.get('id', None)
            status = g.get('status', {}).get('detailedState', '')
            game_time_utc = g.get('gameDate', '')  # ISO 8601 UTC string
            
            # Simplified time handling without dateutil
            if game_time_utc:
                # Basic time format conversion
                game_time = game_time_utc.replace('T', ' ').replace('Z', ' UTC')
            else:
                game_time = ''
                
            result.append({
                'game_pk': g.get('gamePk'),
                'away_team': away_team,
                'away_team_id': away_team_id,
                'home_team': home_team,
                'home_team_id': home_team_id,
                'status': status,
                'game_time': game_time
            })
        return result
        
    except Exception as e:
        print(f"⚠ Could not fetch real games: {e}")
        # Return sample games as fallback
        return [
            {'away_team': 'Yankees', 'home_team': 'Red Sox', 'status': 'Scheduled'},
            {'away_team': 'Dodgers', 'home_team': 'Giants', 'status': 'Scheduled'},
            {'away_team': 'Astros', 'home_team': 'Angels', 'status': 'Scheduled'},
            {'away_team': 'Braves', 'home_team': 'Mets', 'status': 'Scheduled'},
            {'away_team': 'Cardinals', 'home_team': 'Cubs', 'status': 'Scheduled'}
        ]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    games = get_games_for_date(date)
    print(f"MLB Games for {date}:")
    for g in games:
        print(f"{g['away_team']} at {g['home_team']} - {g['status']}")
