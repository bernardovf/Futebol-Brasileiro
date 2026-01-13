# Serie A 2025 Sofascore Crawler

A Python crawler to fetch all **Brasileiro Serie A 2025** match data from Sofascore API for all 20 teams, including minutes played by each player in every match.

## Features

- Fetches matches for all 20 Serie A 2025 teams
- Filters **only Serie A matches** (excludes Copa do Brasil, state championships, etc.)
- Extracts player statistics including minutes played for each match
- **Normalizes both player AND team names** (removes accents and special characters)
- Includes competition/tournament information for each match
- Generates a master player table with detailed player information:
  - Age, height, weight
  - Nationality and position
  - Preferred foot
- Exports data to both CSV and JSON formats
- Avoids duplicate matches when both teams are from Serie A
- Provides detailed summary statistics

## Serie A 2025 Teams (20 Teams)

The crawler includes all 20 teams participating in the 2025 Brasileiro Serie A:

| Team | Sofascore ID |
|------|--------------|
| Botafogo | 1958 |
| Palmeiras | 1685 |
| Flamengo | 1953 |
| São Paulo | 1951 |
| Fortaleza | 1968 |
| Internacional | 1961 |
| Cruzeiro | 1954 |
| Bahia | 1959 |
| Corinthians | 1952 |
| Atlético Mineiro | 1950 |
| Vasco da Gama | 1957 |
| Fluminense | 1956 |
| Grêmio | 1955 |
| Juventude | 1963 |
| RB Bragantino | 13354 |
| Athletico Paranaense | 1960 |
| Criciúma | 1966 |
| Vitória | 2020 |
| Cuiabá | 34911 |
| Atlético Goianiense | 1949 |

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Serie A crawler:
```bash
python serie_a_crawler.py
```

The script will:
1. Fetch all Serie A matches from 2025 for all 20 teams
2. Filter only Serie A competition matches (excludes other tournaments)
3. Extract player minutes for each match
4. Fetch detailed player information
5. Generate four output files:
   - `serie_a_2025_player_minutes.csv` - Match data in CSV format
   - `serie_a_2025_player_minutes.json` - Match data in JSON format
   - `serie_a_2025_players_master.csv` - Player master table in CSV format
   - `serie_a_2025_players_master.json` - Player master table in JSON format

## Output Format

### Match Data (player_minutes files)

The match data includes the following fields for each player in each match:

- `match_id`: Unique match identifier
- `match_date`: Date of the match (YYYY-MM-DD)
- `competition`: Competition/tournament name (e.g., "Brasileiro Serie A")
- `competition_category`: Competition category (e.g., "Brazil")
- `team`: Team name (normalized, without accents)
- `opponent`: Opponent team name (normalized, without accents)
- `home_away`: Whether the team played HOME or AWAY
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
- Tournament: Brasileirão Serie A (Tournament ID: 325)
- API Base: `https://api.sofascore.com/api/v1`

## API Endpoints Used

- Team matches: `/team/{team_id}/events/last/{page}`
- Match lineups: `/event/{match_id}/lineups`
- Player details: `/player/{player_id}`

## Key Features

### Duplicate Prevention
The crawler tracks processed matches to avoid duplicates when both teams in a match are from Serie A.

### Competition Filtering
Only matches from Serie A (Brasileirão) are included. Matches from Copa do Brasil, state championships, and other competitions are automatically excluded.

### Name Normalization
Both player names and team names are normalized:
- "São Paulo" → "Sao Paulo"
- "Atlético Mineiro" → "Atletico Mineiro"
- "Cássio" → "Cassio"

## Notes

- The crawler includes rate limiting (0.5s delay between requests) to be respectful to the API
- This uses an unofficial API - use at your own discretion
- Data is fetched only for Serie A matches played in 2025
- Team IDs may need to be updated if teams change in future seasons

## Example Output

After running the crawler, you'll see output like:

```
Starting Serie A 2025 crawler...
Total teams: 20
======================================================================

Processing team: Botafogo (ID: 1958)
----------------------------------------------------------------------
  Match 1: Botafogo vs Flamengo (2025-04-15)
  Match 2: São Paulo vs Botafogo (2025-04-22)
  ...
Total Serie A matches found for Botafogo: 38

Processing team: Palmeiras (ID: 1685)
----------------------------------------------------------------------
  ...

======================================================================
Total unique matches processed: 380
Total player records extracted: 15000+
======================================================================

DATA SUMMARY
======================================================================
Total unique players: 500+
Total unique matches: 380

Player records by team:
  Atletico Mineiro              :  600 records
  Bahia                         :  590 records
  ...

Top 15 players by total minutes played:
 1. John                               -  3240 minutes
 2. Everson                            -  3150 minutes
 ...

Files generated:
  - serie_a_2025_player_minutes.csv
  - serie_a_2025_player_minutes.json
  - serie_a_2025_players_master.csv
  - serie_a_2025_players_master.json
```

## Utility Scripts

### get_serie_a_teams.py
A utility script to fetch the current Serie A teams and their IDs from the Sofascore API:

```bash
python get_serie_a_teams.py
```

This will create `serie_a_teams.json` with the latest team data.

## Requirements

- Python 3.7+
- requests library

## License

This project is for educational purposes only.

## Related Files

- `main.py` - Original Cruzeiro-only crawler
- `serie_a_crawler.py` - Full Serie A crawler (all 20 teams)
- `get_serie_a_teams.py` - Utility to fetch team IDs
