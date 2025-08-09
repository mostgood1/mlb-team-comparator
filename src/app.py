from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

def get_team_id_by_name(team_name):
    url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    response = requests.get(url)
    teams = response.json()["teams"]
    for team in teams:
        if team_name.lower() == team["name"].lower() or team_name.lower() == team["teamName"].lower():
            return team["id"]
    return None

def get_player_id_by_name(player_name):
    url = f"https://statsapi.mlb.com/api/v1/people/search?names={player_name}"
    response = requests.get(url)
    data = response.json()
    if 'people' in data and data['people']:
        for person in data['people']:
            if player_name.lower() == person['fullName'].lower():
                return person['id']
        return data['people'][0]['id']
    return None

def get_player_stats(player_id, season):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?season={season}&stats=season"
    response = requests.get(url)
    data = response.json()
    try:
        stats = data['stats'][0]['splits'][0]['stat']
    except (KeyError, IndexError):
        return {}
    return stats

def get_team_stats(team_id, season):
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats?season={season}&stats=season"
    response = requests.get(url)
    data = response.json()
    try:
        stats = data['stats'][0]['splits'][0]['stat']
    except (KeyError, IndexError):
        return {}
    return stats

HTML = """
<!doctype html>
<title>MLB Compare Tool</title>
<h1>MLB Compare Tool</h1>
<form method=post>
    <label>Function:</label>
</select><br><br>
    <label>Name:</label>
    <input name=name><br><br>
    <label>Season (for stats):</label>
    <input name=season><br><br>
    <div id="compare" style="display:none;">
        <label>Hitter Name:</label>
        <input name=hitter><br><br>
        <label>Pitcher Name:</label>
        <input name=pitcher><br><br>
        <label>Season:</label>
        <input name=season_compare><br><br>
    </div>
    <input type=submit value=Submit>
    <script>
    document.querySelector('select[name="func"]').addEventListener('change', function(e) {
        document.getElementById('compare').style.display = (e.target.value === 'compare') ? '' : 'none';
    });
    </script>
</form>
{% if result %}
    <h2>Result:</h2>
    {{ result|safe }}
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        func = request.form.get("func")
        name = request.form.get("name")
        season = request.form.get("season")
        if func == "teamid":
            tid = get_team_id_by_name(name)
            result = f"<table border='1'><tr><th>Team Name</th><th>Team ID</th></tr><tr><td>{name}</td><td>{tid if tid else 'Not found'}</td></tr></table>"
        elif func == "playerid":
            pid = get_player_id_by_name(name)
            result = f"<table border='1'><tr><th>Player Name</th><th>Player ID</th></tr><tr><td>{name}</td><td>{pid if pid else 'Not found'}</td></tr></table>"
        elif func == "playerstats":
            pid = get_player_id_by_name(name)
            if pid:
                stats = get_player_stats(pid, season)
                if stats:
                    rows = ''.join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in stats.items()])
                    result = f"<h3>Stats for {name} in {season}:</h3><table border='1'><tr><th>Stat</th><th>Value</th></tr>{rows}</table>"
                else:
                    result = "No stats found."
            else:
                result = "Player not found."
        elif func == "teamstats":
            tid = get_team_id_by_name(name)
            if tid:
                stats = get_team_stats(tid, season)
                if stats:
                    rows = ''.join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in stats.items()])
                    result = f"<h3>Stats for {name} in {season}:</h3><table border='1'><tr><th>Stat</th><th>Value</th></tr>{rows}</table>"
                else:
                    result = "No stats found."
            else:
                result = "Team not found."
        elif func == "compare":
            hitter_name = request.form.get("hitter")
            pitcher_name = request.form.get("pitcher")
            season_compare = request.form.get("season_compare")
            hitter_id = get_player_id_by_name(hitter_name)
            pitcher_id = get_player_id_by_name(pitcher_name)
            hitter_stats = get_player_stats(hitter_id, season_compare) if hitter_id else {}
            pitcher_stats = get_player_stats(pitcher_id, season_compare) if pitcher_id else {}
            # Select key stats for comparison
            hitter_keys = ["avg", "homeRuns", "hits", "atBats", "ops"]
            pitcher_keys = ["era", "strikeOuts", "opponentBattingAvg", "inningsPitched", "whip"]
            rows = ""
            for k in set(hitter_keys + pitcher_keys):
                h_val = hitter_stats.get(k, "-")
                p_val = pitcher_stats.get(k, "-")
                rows += f"<tr><td>{k}</td><td>{h_val}</td><td>{p_val}</td></tr>"

            # Fetch hitter vs pitcher history
            history_url = f"https://statsapi.mlb.com/api/v1/people/{hitter_id}/stats?stats=vsPitcher&season={season_compare}&opposingPlayerId={pitcher_id}"
            history_resp = requests.get(history_url)
            history_data = history_resp.json()
            history_stats = {}
            try:
                history_stats = history_data['stats'][0]['splits'][0]['stat']
            except (KeyError, IndexError):
                history_stats = {}

            history_rows = ''
            if history_stats:
                for k, v in history_stats.items():
                    history_rows += f"<tr><td>{k}</td><td>{v}</td></tr>"
                history_table = f"<h4>Hitter's History vs Pitcher ({season_compare}):</h4><table border='1'><tr><th>Stat</th><th>Value</th></tr>{history_rows}</table>"
            else:
                history_table = "<h4>No hitter vs pitcher history found for this season.</h4>"

            result = f"<h3>Comparison: {hitter_name} vs {pitcher_name} ({season_compare})</h3>"
            result += "<table border='1'><tr><th>Stat</th><th>Hitter</th><th>Pitcher</th></tr>" + rows + "</table>"
            result += history_table
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)