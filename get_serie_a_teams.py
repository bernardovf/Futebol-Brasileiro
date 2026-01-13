"""
Script to fetch all Serie A 2025 team IDs from Sofascore API.
"""

import requests
import json

def get_serie_a_teams():
    """
    Fetch all teams participating in Serie A 2025.
    """
    # Serie A tournament ID: 325
    # Season ID for 2025: 61644 (you may need to verify this)

    base_url = "https://api.sofascore.com/api/v1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }

    # Try to get current season standings
    tournament_id = 325  # Serie A

    # First, get the current season info
    season_url = f"{base_url}/unique-tournament/{tournament_id}/seasons"

    try:
        response = requests.get(season_url, headers=headers, timeout=10)
        response.raise_for_status()
        seasons_data = response.json()

        print("Available seasons:")
        seasons = seasons_data.get('seasons', [])
        for season in seasons[:5]:  # Show last 5 seasons
            print(f"  Season: {season.get('year')} - ID: {season.get('id')}")

        # Get the most recent season (likely 2025)
        if seasons:
            current_season_id = seasons[0].get('id')
            print(f"\nUsing season ID: {current_season_id}")

            # Get standings for this season
            standings_url = f"{base_url}/unique-tournament/{tournament_id}/season/{current_season_id}/standings/total"

            response = requests.get(standings_url, headers=headers, timeout=10)
            response.raise_for_status()
            standings_data = response.json()

            teams = []

            # Extract teams from standings
            for standing_group in standings_data.get('standings', []):
                for row in standing_group.get('rows', []):
                    team = row.get('team', {})
                    teams.append({
                        'id': team.get('id'),
                        'name': team.get('name'),
                        'shortName': team.get('shortName', '')
                    })

            print(f"\nFound {len(teams)} teams in Serie A 2025:\n")
            print("=" * 70)

            for idx, team in enumerate(teams, 1):
                print(f"{idx:2d}. {team['name']:30s} (ID: {team['id']:6d}) - {team['shortName']}")

            print("=" * 70)

            # Save to file
            with open('serie_a_teams.json', 'w', encoding='utf-8') as f:
                json.dump(teams, f, indent=2, ensure_ascii=False)

            print(f"\nTeam data saved to serie_a_teams.json")

            return teams

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    teams = get_serie_a_teams()
