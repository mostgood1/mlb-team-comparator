// MLB Teams data
const MLB_TEAMS = [
    "Angels", "Astros", "Athletics", "Blue Jays", "Braves", "Brewers", "Cardinals", 
    "Cubs", "Diamondbacks", "Dodgers", "Giants", "Guardians", "Mariners", "Marlins", 
    "Mets", "Nationals", "Orioles", "Padres", "Phillies", "Pirates", "Rangers", 
    "Rays", "Red Sox", "Reds", "Rockies", "Royals", "Tigers", "Twins", "White Sox", "Yankees"
];

// Populate team dropdowns
function populateTeamDropdowns() {
    const awaySelect = document.getElementById('awayTeam');
    const homeSelect = document.getElementById('homeTeam');
    
    MLB_TEAMS.forEach(team => {
        const awayOption = document.createElement('option');
        awayOption.value = team;
        awayOption.textContent = team;
        awaySelect.appendChild(awayOption);
        
        const homeOption = document.createElement('option');
        homeOption.value = team;
        homeOption.textContent = team;
        homeSelect.appendChild(homeOption);
    });
}

// Initialize dropdowns when page loads
document.addEventListener('DOMContentLoaded', populateTeamDropdowns);
