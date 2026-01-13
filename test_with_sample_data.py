"""
Test script with sample data to demonstrate the crawler functionality.
This simulates what the crawler would return with real API data.
"""

import json
import csv
from datetime import datetime

# Sample data structure based on Sofascore API responses
SAMPLE_MATCHES = [
    {
        'id': 12345678,
        'startTimestamp': 1704585600,  # 2025-01-07
        'homeTeam': {'id': 1954, 'name': 'Cruzeiro'},
        'awayTeam': {'id': 1234, 'name': 'Atlético Mineiro'},
        'homeScore': {'current': 2},
        'awayScore': {'current': 1}
    },
    {
        'id': 12345679,
        'startTimestamp': 1705190400,  # 2025-01-14
        'homeTeam': {'id': 5678, 'name': 'Flamengo'},
        'awayTeam': {'id': 1954, 'name': 'Cruzeiro'},
        'homeScore': {'current': 1},
        'awayScore': {'current': 1}
    },
    {
        'id': 12345680,
        'startTimestamp': 1705795200,  # 2025-01-21
        'homeTeam': {'id': 1954, 'name': 'Cruzeiro'},
        'awayTeam': {'id': 9012, 'name': 'Palmeiras'},
        'homeScore': {'current': 3},
        'awayScore': {'current': 0}
    }
]

SAMPLE_LINEUPS = {
    12345678: {
        'home': {
            'players': [
                {
                    'player': {'id': 101, 'name': 'Cássio'},
                    'position': 'G',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '1'
                },
                {
                    'player': {'id': 102, 'name': 'William'},
                    'position': 'D',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '3'
                },
                {
                    'player': {'id': 103, 'name': 'Lucas Romero'},
                    'position': 'M',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '8'
                },
                {
                    'player': {'id': 104, 'name': 'Matheus Pereira'},
                    'position': 'M',
                    'statistics': {'minutesPlayed': 75},
                    'substitute': False,
                    'shirtNumber': '10'
                },
                {
                    'player': {'id': 105, 'name': 'Kaio Jorge'},
                    'position': 'F',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '9'
                },
                {
                    'player': {'id': 106, 'name': 'Gabriel Veron'},
                    'position': 'F',
                    'statistics': {'minutesPlayed': 15},
                    'substitute': True,
                    'shirtNumber': '11'
                }
            ]
        }
    },
    12345679: {
        'away': {
            'players': [
                {
                    'player': {'id': 101, 'name': 'Cássio'},
                    'position': 'G',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '1'
                },
                {
                    'player': {'id': 102, 'name': 'William'},
                    'position': 'D',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '3'
                },
                {
                    'player': {'id': 103, 'name': 'Lucas Romero'},
                    'position': 'M',
                    'statistics': {'minutesPlayed': 85},
                    'substitute': False,
                    'shirtNumber': '8'
                },
                {
                    'player': {'id': 104, 'name': 'Matheus Pereira'},
                    'position': 'M',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '10'
                },
                {
                    'player': {'id': 105, 'name': 'Kaio Jorge'},
                    'position': 'F',
                    'statistics': {'minutesPlayed': 60},
                    'substitute': False,
                    'shirtNumber': '9'
                },
                {
                    'player': {'id': 107, 'name': 'Rafa Silva'},
                    'position': 'F',
                    'statistics': {'minutesPlayed': 30},
                    'substitute': True,
                    'shirtNumber': '7'
                }
            ]
        }
    },
    12345680: {
        'home': {
            'players': [
                {
                    'player': {'id': 101, 'name': 'Cássio'},
                    'position': 'G',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '1'
                },
                {
                    'player': {'id': 102, 'name': 'William'},
                    'position': 'D',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '3'
                },
                {
                    'player': {'id': 103, 'name': 'Lucas Romero'},
                    'position': 'M',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '8'
                },
                {
                    'player': {'id': 104, 'name': 'Matheus Pereira'},
                    'position': 'M',
                    'statistics': {'minutesPlayed': 80},
                    'substitute': False,
                    'shirtNumber': '10'
                },
                {
                    'player': {'id': 105, 'name': 'Kaio Jorge'},
                    'position': 'F',
                    'statistics': {'minutesPlayed': 90},
                    'substitute': False,
                    'shirtNumber': '9'
                },
                {
                    'player': {'id': 106, 'name': 'Gabriel Veron'},
                    'position': 'F',
                    'statistics': {'minutesPlayed': 10},
                    'substitute': True,
                    'shirtNumber': '11'
                }
            ]
        }
    }
}


def extract_player_minutes(lineups, match_info):
    """Extract minutes played by each player from lineup data."""
    players_data = []

    if not lineups:
        return players_data

    match_id = match_info.get('id')
    match_date = datetime.fromtimestamp(match_info.get('startTimestamp', 0)).strftime('%Y-%m-%d')
    home_team = match_info.get('homeTeam', {}).get('name', 'Unknown')
    away_team = match_info.get('awayTeam', {}).get('name', 'Unknown')
    home_score = match_info.get('homeScore', {}).get('current', 0)
    away_score = match_info.get('awayScore', {}).get('current', 0)

    # Determine if Cruzeiro was home or away
    cruzeiro_side = None
    if home_team == 'Cruzeiro' or match_info.get('homeTeam', {}).get('id') == 1954:
        cruzeiro_side = 'home'
        opponent = away_team
        result = 'W' if home_score > away_score else ('D' if home_score == away_score else 'L')
    elif away_team == 'Cruzeiro' or match_info.get('awayTeam', {}).get('id') == 1954:
        cruzeiro_side = 'away'
        opponent = home_team
        result = 'W' if away_score > home_score else ('D' if home_score == away_score else 'L')

    if not cruzeiro_side:
        return players_data

    # Get Cruzeiro's lineup
    cruzeiro_lineup = lineups.get(cruzeiro_side, {})

    # Extract players from starting XI
    if 'players' in cruzeiro_lineup:
        for player in cruzeiro_lineup['players']:
            player_info = player.get('player', {})
            statistics = player.get('statistics', {})

            players_data.append({
                'match_id': match_id,
                'match_date': match_date,
                'opponent': opponent,
                'home_away': cruzeiro_side.upper(),
                'score': f"{home_score}-{away_score}",
                'result': result,
                'player_id': player_info.get('id'),
                'player_name': player_info.get('name'),
                'position': player.get('position', 'Unknown'),
                'minutes_played': statistics.get('minutesPlayed', 0),
                'substitute': player.get('substitute', False),
                'shirt_number': player.get('shirtNumber', '')
            })

    return players_data


def main():
    """Run test with sample data."""
    print("Testing Cruzeiro crawler with sample data...")
    print("=" * 60)

    all_player_data = []

    # Process each sample match
    for match in SAMPLE_MATCHES:
        match_id = match['id']
        match_date = datetime.fromtimestamp(match['startTimestamp']).strftime('%Y-%m-%d')
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']

        print(f"Processing: {home_team} vs {away_team} ({match_date})")

        # Get lineups for this match
        lineups = SAMPLE_LINEUPS.get(match_id, {})
        player_data = extract_player_minutes(lineups, match)
        all_player_data.extend(player_data)

    print("\n" + "=" * 60)
    print(f"Total player records: {len(all_player_data)}")
    print("=" * 60)

    # Calculate summary statistics
    unique_players = set(p['player_name'] for p in all_player_data)
    print(f"\nUnique players: {len(unique_players)}")
    print(f"Total matches: {len(SAMPLE_MATCHES)}")

    # Total minutes by player
    player_total_minutes = {}
    for record in all_player_data:
        name = record['player_name']
        minutes = record['minutes_played']
        player_total_minutes[name] = player_total_minutes.get(name, 0) + minutes

    print(f"\nPlayers by total minutes played:")
    sorted_players = sorted(player_total_minutes.items(), key=lambda x: x[1], reverse=True)
    for idx, (player, minutes) in enumerate(sorted_players, 1):
        print(f"{idx:2d}. {player:30s} - {minutes:4d} minutes")

    # Save to CSV
    csv_filename = "sample_cruzeiro_2025_player_minutes.csv"
    fieldnames = [
        'match_id', 'match_date', 'opponent', 'home_away', 'score', 'result',
        'player_id', 'player_name', 'position', 'minutes_played',
        'substitute', 'shirt_number'
    ]

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_player_data)

    print(f"\nData saved to {csv_filename}")

    # Save to JSON
    json_filename = "sample_cruzeiro_2025_player_minutes.json"
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_player_data, jsonfile, indent=2, ensure_ascii=False)

    print(f"Data saved to {json_filename}")

    # Display sample of the data
    print("\n" + "=" * 60)
    print("Sample data (first 5 records):")
    print("=" * 60)
    for record in all_player_data[:5]:
        print(f"\nMatch: {record['match_date']} vs {record['opponent']} ({record['home_away']})")
        print(f"Player: {record['player_name']} (#{record['shirt_number']})")
        print(f"Position: {record['position']}, Minutes: {record['minutes_played']}")
        print(f"Substitute: {record['substitute']}, Result: {record['result']}")

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
