# Brazilian Football Sofascore Crawlers

Python crawlers to fetch Brazilian football match data from Sofascore API for the 2025 season, including minutes played by each player in every match.

## Available Crawlers

| Crawler | Teams | Competitions | Team Names Normalized | Output Files |
|---------|-------|--------------|----------------------|--------------|
| **`main.py`** | Cruzeiro only | All (Serie A, Copa do Brasil, etc.) | No | `cruzeiro_2025_*.csv/json` |
| **`serie_a_crawler.py`** | All 20 Serie A teams | Serie A only | Yes | `serie_a_2025_*.csv/json` |

For the **Serie A crawler** documentation, see **[README_SERIE_A.md](README_SERIE_A.md)**.

---

# Cruzeiro Sofascore Crawler (main.py)

A Python crawler to fetch Cruzeiro's match data from Sofascore API for the 2025 season, including minutes played by each player in every match.

## Features

- Fetches all Cruzeiro matches from 2025
- Extracts player statistics including minutes played for each match
- Includes competition/tournament information for each match
- Normalizes player names (removes accents and special characters)
- Generates a master player table with detailed player information:
  - Age, height, weight
  - Nationality and position
  - Preferred foot
- Exports data to both CSV and JSON formats
- Provides summary statistics

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the crawler:
```bash
python main.py
```

The script will:
1. Fetch all Cruzeiro matches from 2025
2. Extract player minutes for each match
3. Fetch detailed player information
4. Generate four output files:
   - `cruzeiro_2025_player_minutes.csv` - Match data in CSV format
   - `cruzeiro_2025_player_minutes.json` - Match data in JSON format
   - `cruzeiro_2025_players_master.csv` - Player master table in CSV format
   - `cruzeiro_2025_players_master.json` - Player master table in JSON format

## Output Format

### Match Data (player_minutes files)

The match data includes the following fields for each player in each match:

- `match_id`: Unique match identifier
- `match_date`: Date of the match (YYYY-MM-DD)
- `competition`: Competition/tournament name (e.g., "Brasileiro Serie A", "Copa do Brasil")
- `competition_category`: Competition category (e.g., "Brazil")
- `opponent`: Opponent team name
- `home_away`: Whether Cruzeiro played HOME or AWAY
- `score`: Match score
- `result`: W (Win), D (Draw), or L (Loss)
- `player_id`: Unique player identifier
- `player_name`: Player's name (normalized, without accents)
- `position`: Player's position on the field
- `minutes_played`: Minutes played in the match
- `substitute`: Whether the player started as a substitute
- `shirt_number`: Player's shirt number

### Player Master Table (players_master files)

The player master table includes the following fields for each unique player:

- `player_id`: Unique player identifier
- `player_name`: Player's name (normalized, without accents)
- `age`: Player's age in years
- `height`: Player's height in centimeters
- `weight`: Player's weight in kilograms
- `nationality`: Player's nationality
- `position`: Primary playing position
- `preferred_foot`: Preferred foot (Left/Right)
- `market_value`: Market value (Note: Not available in Sofascore API, field will be empty)

## Data Source

This crawler uses the unofficial Sofascore API endpoints. The data is fetched from:
- Team: Cruzeiro (Team ID: 1954)
- API Base: `https://api.sofascore.com/api/v1`

## API Endpoints Used

- Team matches: `/team/{team_id}/events/last/{page}`
- Match lineups: `/event/{match_id}/lineups`
- Player details: `/player/{player_id}`

## Notes

- The crawler includes rate limiting (0.5s delay between requests) to be respectful to the API
- This uses an unofficial API - use at your own discretion
- Data is fetched only for matches played in 2025

## Example Output

After running the crawler, you'll see a summary like:

```
Total unique players: 35
Total matches: 15

Top 10 players by total minutes played:
 1. Cassio                        - 1350 minutes
 2. William                       - 1320 minutes
 3. Lucas Romero                  - 1200 minutes
...

Fetching player details for master table...
Successfully fetched details for 35 players

Files generated:
  - cruzeiro_2025_player_minutes.csv
  - cruzeiro_2025_player_minutes.json
  - cruzeiro_2025_players_master.csv
  - cruzeiro_2025_players_master.json
```

Note: Player names are normalized (e.g., "Cássio" becomes "Cassio")

## Requirements

- Python 3.7+
- requests library

## License

This project is for educational purposes only.
