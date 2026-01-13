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

⚠️ **IMPORTANT**: The crawler now includes verified team IDs for 13 teams. Remaining teams need verification.

The crawler is configured for the **2025 Brasileirão Betano** with 18 confirmed teams (2 missing from official 20-team roster):

### Verified Team IDs ✅

| Position | Team | Sofascore ID | Verified URL |
|----------|------|--------------|--------------|
| 1º | Flamengo [Campeão] | 5981 | https://www.sofascore.com/football/team/flamengo/5981 |
| 2º | Palmeiras | 1963 | https://sofascore.com/team/football/palmeiras/1963 |
| 3º | Cruzeiro | 1954 | Already verified |
| 4º | Mirassol | 21982 | https://www.sofascore.com/football/team/mirassol/21982 |
| 6º | Botafogo | 1958 | https://www.sofascore.com/team/football/botafogo/1958 |
| 7º | Bahia | 1955 | https://www.sofascore.com/team/football/bahia/1955 |
| 9º | Grêmio | 5926 | https://www.sofascore.com/football/team/gremio/5926 |
| 12º | Santos | 1968 | https://www.sofascore.com/football/team/santos/1968 |
| 13º | Corinthians | 1957 | https://sofascore.com/team/football/corinthians/1957 |
| 14º | Vasco | 1974 | https://www.sofascore.com/team/football/vasco-da-gama/1974 |
| 17º | Ceará | 2001 | https://www.sofascore.com/football/team/ceara/2001 |
| 18º | Fortaleza | 2020 | https://www.sofascore.com/team/football/fortaleza/2020 |
| 20º | Sport | 1959 | https://www.sofascore.com/football/team/sport-recife/1959 |

### Needs Verification ⚠️

| Position | Team | Current ID | Notes |
|----------|------|------------|-------|
| 5º | Fluminense | 1956 | Needs verification |
| 8º | São Paulo | 1951 | Needs verification |
| 10º | RB Bragantino | 13354 | Needs verification |
| 11º | Atlético Mineiro | 1950 | Needs verification |
| 19º | Juventude | 1963 | ⚠️ CONFLICTS with Palmeiras! Must verify |

### Missing Teams

2 teams from the official 20-team roster are missing. Please verify the complete 2025 Brasileirão Betano standings.

**How to Verify Team IDs:**
1. Go to [Sofascore.com](https://www.sofascore.com)
2. Search for the team name (e.g., "Internacional Brazil")
3. Click on the team page
4. Check the URL: `sofascore.com/team/football/{TEAM_NAME}/{TEAM_ID}`
5. Update the ID in `serie_a_crawler.py` if needed

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

### Expected Match Count

The crawler verifies that it's collecting the correct number of matches:
- **Full Serie A season**: 380 matches (20 teams × 19 rounds × 2)
- The crawler will warn if fewer matches are found, which could indicate:
  - Season not yet complete
  - Incorrect team IDs
  - Missing teams from the configuration

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
**Only matches from Brasileirão Betano (Serie A) are included.**

The filter specifically excludes:
- Copa do Brasil
- State championships (Paulista, Carioca, Mineiro, Gaúcho, Pernambucano, Baiano, Cearense)
- Serie B
- Other tournaments

The filter checks for:
- Tournament name containing "Brasileiro", "Brasileirão", or "Brasileirao"
- Tournament slug matching "brasileirao"
- Excludes matches with state championship or cup keywords

### Match Count Verification
The crawler automatically verifies the total match count:
- **Expected**: 380 matches for a complete Serie A season
- **Formula**: 20 teams × 19 rounds × 2 = 380 matches
- Displays warning if match count is below expected

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
