"""
Test script with sample data to demonstrate the crawler functionality.
This simulates what the crawler would return with real API data.
"""

import json
import csv
from datetime import datetime
import unicodedata


def normalize_text(text: str) -> str:
    """
    Remove special characters and accents from text.

    Args:
        text: Text to normalize

    Returns:
        Normalized text without accents
    """
    if not text:
        return text
    # Normalize to NFD (decomposed form) and filter out combining characters
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

# Sample data structure based on Sofascore API responses
SAMPLE_MATCHES = [
    {
        'id': 12345678,
        'startTimestamp': 1704585600,  # 2025-01-07
        'homeTeam': {'id': 1954, 'name': 'Cruzeiro'},
        'awayTeam': {'id': 1234, 'name': 'Atlético Mineiro'},
        'homeScore': {'current': 2},
        'awayScore': {'current': 1},
        'tournament': {
            'name': 'Campeonato Mineiro',
            'category': {'name': 'Brazil'}
        }
    },
    {
        'id': 12345679,
        'startTimestamp': 1705190400,  # 2025-01-14
        'homeTeam': {'id': 5678, 'name': 'Flamengo'},
        'awayTeam': {'id': 1954, 'name': 'Cruzeiro'},
        'homeScore': {'current': 1},
        'awayScore': {'current': 1},
        'tournament': {
            'name': 'Brasileiro Serie A',
            'category': {'name': 'Brazil'}
        }
    },
    {
        'id': 12345680,
        'startTimestamp': 1705795200,  # 2025-01-21
        'homeTeam': {'id': 1954, 'name': 'Cruzeiro'},
        'awayTeam': {'id': 9012, 'name': 'Palmeiras'},
        'homeScore': {'current': 3},
        'awayScore': {'current': 0},
        'tournament': {
            'name': 'Copa do Brasil',
            'category': {'name': 'Brazil'}
        }
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
                    'player': {'id': 106, 'name': 'Gabriel Verón'},
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
                    'player': {'id': 106, 'name': 'Gabriel Verón'},
                    'position': 'F',
                    'statistics': {'minutesPlayed': 10},
                    'substitute': True,
                    'shirtNumber': '11'
                }
            ]
        }
    }
}

# Sample player master data
SAMPLE_PLAYER_MASTER = {
    101: {'id': 101, 'name': 'Cássio', 'age': 37, 'height': 195, 'weight': 84, 'nationality': 'Brazil', 'position': 'G', 'preferred_foot': 'Right'},
    102: {'id': 102, 'name': 'William', 'age': 29, 'height': 184, 'weight': 78, 'nationality': 'Brazil', 'position': 'D', 'preferred_foot': 'Right'},
    103: {'id': 103, 'name': 'Lucas Romero', 'age': 30, 'height': 180, 'weight': 74, 'nationality': 'Argentina', 'position': 'M', 'preferred_foot': 'Right'},
    104: {'id': 104, 'name': 'Matheus Pereira', 'age': 28, 'height': 177, 'weight': 73, 'nationality': 'Brazil', 'position': 'M', 'preferred_foot': 'Left'},
    105: {'id': 105, 'name': 'Kaio Jorge', 'age': 23, 'height': 183, 'weight': 76, 'nationality': 'Brazil', 'position': 'F', 'preferred_foot': 'Right'},
    106: {'id': 106, 'name': 'Gabriel Verón', 'age': 22, 'height': 172, 'weight': 68, 'nationality': 'Brazil', 'position': 'F', 'preferred_foot': 'Left'},
    107: {'id': 107, 'name': 'Rafa Silva', 'age': 31, 'height': 170, 'weight': 65, 'nationality': 'Portugal', 'position': 'F', 'preferred_foot': 'Right'},
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

    # Extract competition/tournament information
    tournament = match_info.get('tournament', {})
    competition_name = tournament.get('name', 'Unknown')
    competition_category = tournament.get('category', {}).get('name', 'Unknown')

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
            player_name = normalize_text(player_info.get('name', ''))

            players_data.append({
                'match_id': match_id,
                'match_date': match_date,
                'competition': competition_name,
                'competition_category': competition_category,
                'opponent': opponent,
                'home_away': cruzeiro_side.upper(),
                'score': f"{home_score}-{away_score}",
                'result': result,
                'player_id': player_info.get('id'),
                'player_name': player_name,
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
    unique_player_ids = set()

    # Process each sample match
    for match in SAMPLE_MATCHES:
        match_id = match['id']
        match_date = datetime.fromtimestamp(match['startTimestamp']).strftime('%Y-%m-%d')
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        competition = match['tournament']['name']

        print(f"Processing: {home_team} vs {away_team} ({match_date}) - {competition}")

        # Get lineups for this match
        lineups = SAMPLE_LINEUPS.get(match_id, {})
        player_data = extract_player_minutes(lineups, match)
        all_player_data.extend(player_data)

        # Track unique players
        for record in player_data:
            unique_player_ids.add(record['player_id'])

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

    # Save match data to CSV
    csv_filename = "sample_cruzeiro_2025_player_minutes.csv"
    fieldnames = [
        'match_id', 'match_date', 'competition', 'competition_category',
        'opponent', 'home_away', 'score', 'result',
        'player_id', 'player_name', 'position', 'minutes_played',
        'substitute', 'shirt_number'
    ]

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_player_data)

    print(f"\nMatch data saved to {csv_filename}")

    # Save match data to JSON
    json_filename = "sample_cruzeiro_2025_player_minutes.json"
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_player_data, jsonfile, indent=2, ensure_ascii=False)

    print(f"Match data saved to {json_filename}")

    # Generate player master table
    print("\n" + "=" * 60)
    print("Generating player master table...")
    print("=" * 60)

    player_master_data = []
    for player_id in unique_player_ids:
        player_info = SAMPLE_PLAYER_MASTER.get(player_id, {})
        if player_info:
            player_master_data.append({
                'player_id': player_info['id'],
                'player_name': normalize_text(player_info['name']),
                'age': player_info.get('age'),
                'height': player_info.get('height'),
                'weight': player_info.get('weight'),
                'nationality': player_info.get('nationality'),
                'position': player_info.get('position'),
                'preferred_foot': player_info.get('preferred_foot'),
                'market_value': None  # Not available in Sofascore API
            })

    # Save player master to CSV
    master_csv_filename = "sample_cruzeiro_2025_players_master.csv"
    master_fieldnames = [
        'player_id', 'player_name', 'age', 'height', 'weight',
        'nationality', 'position', 'preferred_foot', 'market_value'
    ]

    with open(master_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=master_fieldnames)
        writer.writeheader()
        writer.writerows(player_master_data)

    print(f"Player master data saved to {master_csv_filename}")

    # Save player master to JSON
    master_json_filename = "sample_cruzeiro_2025_players_master.json"
    with open(master_json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(player_master_data, jsonfile, indent=2, ensure_ascii=False)

    print(f"Player master data saved to {master_json_filename}")

    # Display sample of the data
    print("\n" + "=" * 60)
    print("Sample match data (first 5 records):")
    print("=" * 60)
    for record in all_player_data[:5]:
        print(f"\nMatch: {record['match_date']} vs {record['opponent']} ({record['home_away']})")
        print(f"Competition: {record['competition']} ({record['competition_category']})")
        print(f"Player: {record['player_name']} (#{record['shirt_number']})")
        print(f"Position: {record['position']}, Minutes: {record['minutes_played']}")
        print(f"Substitute: {record['substitute']}, Result: {record['result']}")

    # Display player master data
    print("\n" + "=" * 60)
    print("Player master table:")
    print("=" * 60)
    for player in player_master_data:
        print(f"\n{player['player_name']} (ID: {player['player_id']})")
        print(f"  Age: {player['age']}, Height: {player['height']}cm, Weight: {player['weight']}kg")
        print(f"  Nationality: {player['nationality']}, Position: {player['position']}")
        print(f"  Preferred Foot: {player['preferred_foot']}")

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)
    print(f"\nFiles generated:")
    print(f"  - {csv_filename}")
    print(f"  - {json_filename}")
    print(f"  - {master_csv_filename}")
    print(f"  - {master_json_filename}")
    print("=" * 60)


if __name__ == "__main__":
    main()
