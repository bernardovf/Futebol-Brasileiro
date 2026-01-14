"""
Direct Match Lineup Fetcher
Fetches lineup data directly from a list of match IDs
"""

import requests
import json
import csv
from datetime import datetime
import time
from typing import List, Dict
import unicodedata


def normalize_text(text: str) -> str:
    """Remove special characters and accents from text."""
    if not text:
        return text
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')


# All Serie A 2025 match IDs provided by user
MATCH_IDS = [
    13472903, 13472668, 13472686, 13472722, 13472724, 13472747, 13472763, 13472796,
    13472802, 13472820, 13472847, 13472665, 13472710, 13472740, 14933649, 13472783,
    13472588, 13472615, 13472620, 13472593, 13473364, 13473368, 13473379, 13473388,
    13473403, 13473408, 13473418, 13473430, 13472675, 13472758, 13472811, 13472836,
    13472859, 13472865, 13472883, 13472886, 13473338, 13473355, 13472898, 13472671,
    13472689, 13472709, 13472728, 13472756, 13472767, 13472788, 14693875, 13472805,
    13472838, 13472694, 13472706, 13472757, 14863346, 13472623, 13472597, 13472616,
    15121158, 13472591, 13473360, 13473374, 13473386, 13473390, 13473399, 13473410,
    13473422, 13472696, 13472807, 13472842, 13472855, 13472867, 13472882, 13472888,
    13473340, 13473357, 13472857, 13472870, 13472876, 13472891, 13472901, 13472676,
    13472695, 13472718, 13472734, 13472745, 13472792, 13472810, 13472828, 13472677,
    13472723, 13472761, 13472821, 13472594, 13472618, 13472634, 13472633, 13473343,
    13473354, 13473361, 13473373, 13473382, 13473393, 13473417, 13473423, 13473437,
    13472746, 13472778, 13472798, 13472850, 13472848, 13472863, 13472869, 13472879,
    13472682, 13472693, 13472717, 14550035, 13472732, 13472753, 13472770, 13472785,
    14689171, 13472809, 13472827, 13472849, 13472672, 13472698, 13472795, 13472612,
    13472617, 13472621, 13473352, 13473365, 13473372, 13473387, 13473392, 13473402,
    13473412, 13473424, 13473431, 13472692, 13472894, 13472683, 13472687, 13472711,
    13472726, 14549632, 13472743, 13472764, 13472793, 13472832, 13472837, 13472702,
    13472769, 13472787, 13472603, 13472611, 13472610, 13473349, 13473362, 13473369,
    13473383, 13473389, 13473405, 13473409, 13472688, 13788130, 13472762, 13472803,
    13472854, 13472866, 13472884, 13472893, 13472899, 13472679, 13472739, 14543946,
    13472814, 13472831, 14689179, 13472840, 13472685, 13472719, 13472765, 13472813,
    13472595, 13472619, 13472598, 13472602, 13473345, 13473351, 13473385, 13473425,
    13473435, 13472704, 13472733, 13472786, 13472853, 13472872, 13472877, 13472895,
    13472670, 13472705, 13472742, 13472773, 13472806, 13472824, 13472846, 13472667,
    13472715, 13472748, 13472791, 13472590, 13472600, 13473350, 13473370, 13473380,
    13473400, 13473420, 13473434, 13472684, 13472741, 13472766, 13472829, 13472845,
    13472887, 13472900, 14333880, 13472703, 13472707, 13472784, 13472816, 13472822,
    13472841, 13472666, 13472744, 13472808, 13472606, 13472596, 13473339, 13473359,
    13473376, 13473415, 13473419, 13473428, 13472680, 13472729, 13472839, 13472871,
    13472905, 13472678, 13472701, 13472749, 13472776, 13472797, 13472818, 13472843,
    14824794, 13472690, 13472731, 13472817, 13473342, 13473356, 13473367, 13473396,
    13473406, 13473411, 13473426, 13472708, 13472790, 13472851, 13472896, 13472697,
    13472721, 13472759, 13472777, 13472799, 13472669, 13472774, 15011357, 13472614,
    13472608, 13473346, 13473366, 13473375, 13473397, 13473401, 13473416, 13472750,
    13472873, 13472823, 13472794, 13472862, 13472874, 13472892, 13472906, 13472713,
    13472780, 14689178, 13472830, 13472736, 13472779, 13472609, 13472613, 13472607,
    13473341, 13473377, 13473398, 13473438, 13472875, 13472902, 13472735, 13472755,
    13472768, 13472789, 13472812, 13472844, 13472604, 13473344, 13473384, 13473395,
    13473404, 13473414, 13473421, 13472712, 13472858, 13472878, 13472691, 13472714,
    13472730, 13472751, 13472825, 13472601, 13472584, 13473358, 13473371, 13473381,
    13473391, 13473436, 13472674, 13472738, 13472781, 13472801, 13472835, 13472605,
    13473378, 13473413, 13473427, 13472700, 13472868, 13473348, 13472864, 13472881,
    13472889, 13472673, 13472752, 13472589, 13472599, 13472635, 13473353, 13472815,
    13472852, 13472880, 13472890, 13472834, 13472632, 15121159, 13472592, 13473432,
    13472699, 13472772, 13472681, 13473363, 13473407, 13472737, 13472760, 13473347,
    13473394, 13472904, 13472782, 13472727
]


class DirectMatchFetcher:
    """Fetches lineup data directly from match IDs."""

    def __init__(self):
        self.base_url = "https://api.sofascore.com/api/v1"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        self.player_minutes = []
        self.players_master = {}
        self.skipped_matches = []

    def get_match_details(self, match_id: int) -> Dict:
        """Fetch match details."""
        url = f"{self.base_url}/event/{match_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json().get('event', {})
        except requests.exceptions.RequestException as e:
            print(f"Error fetching match details for {match_id}: {e}")
            return {}

    def get_match_lineups(self, match_id: int) -> Dict:
        """Fetch lineups for a specific match."""
        url = f"{self.base_url}/event/{match_id}/lineups"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None  # Postponed/not played yet
            print(f"HTTP error fetching lineups for match {match_id}: {e}")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching lineups for match {match_id}: {e}")
            return {}

    def get_player_details(self, player_id: int) -> Dict:
        """Fetch detailed information for a specific player."""
        url = f"{self.base_url}/player/{player_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            player = data.get('player', {})

            # Calculate age from date of birth
            age = None
            if 'dateOfBirthTimestamp' in player:
                birth_date = datetime.fromtimestamp(player['dateOfBirthTimestamp'])
                today = datetime.now()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            return {
                'player_id': player.get('id'),
                'player_name': normalize_text(player.get('name', '')),
                'age': age,
                'height': player.get('height'),
                'weight': player.get('weight'),
                'nationality': player.get('country', {}).get('name', ''),
                'position': player.get('position', ''),
                'preferred_foot': player.get('preferredFoot', ''),
                'market_value': None
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching player details for player {player_id}: {e}")
            return {}

    def extract_player_minutes(self, lineups: Dict, match_info: Dict) -> List[Dict]:
        """Extract minutes played by each player from lineup data."""
        players_data = []

        if not lineups:
            return players_data

        match_id = match_info.get('id')
        match_date = datetime.fromtimestamp(match_info.get('startTimestamp', 0)).strftime('%Y-%m-%d')
        home_team = normalize_text(match_info.get('homeTeam', {}).get('name', 'Unknown'))
        away_team = normalize_text(match_info.get('awayTeam', {}).get('name', 'Unknown'))
        home_score = match_info.get('homeScore', {}).get('current', 0)
        away_score = match_info.get('awayScore', {}).get('current', 0)

        # Extract competition/tournament information
        tournament = match_info.get('tournament', {})
        competition_name = tournament.get('name', 'Unknown')
        competition_category = tournament.get('category', {}).get('name', 'Unknown')

        # Process both home and away teams
        for side in ['home', 'away']:
            team_lineup = lineups.get(side, {})

            if side == 'home':
                team_name = home_team
                opponent = away_team
                result = 'W' if home_score > away_score else ('D' if home_score == away_score else 'L')
            else:
                team_name = away_team
                opponent = home_team
                result = 'W' if away_score > home_score else ('D' if home_score == away_score else 'L')

            # Extract players from lineup
            if 'players' in team_lineup:
                for player in team_lineup['players']:
                    player_info = player.get('player', {})
                    statistics = player.get('statistics', {})
                    player_id = player_info.get('id')
                    player_name = normalize_text(player_info.get('name', ''))

                    players_data.append({
                        'match_id': match_id,
                        'match_date': match_date,
                        'competition': competition_name,
                        'competition_category': competition_category,
                        'team': team_name,
                        'opponent': opponent,
                        'home_away': side.upper(),
                        'score': f"{home_score}-{away_score}",
                        'result': result,
                        'player_id': player_id,
                        'player_name': player_name,
                        'position': player.get('position', 'Unknown'),
                        'minutes_played': statistics.get('minutesPlayed', 0),
                        'substitute': player.get('substitute', False),
                        'shirt_number': player.get('shirtNumber', '')
                    })

                    # Track unique players for master table
                    if player_id and player_id not in self.players_master:
                        self.players_master[player_id] = player_name

        return players_data

    def fetch_all_matches(self, match_ids: List[int]):
        """Fetch lineups for all match IDs."""
        print("Starting direct match lineup fetcher...")
        print(f"Total matches to fetch: {len(match_ids)}")
        print("=" * 70)

        for idx, match_id in enumerate(match_ids, 1):
            print(f"\n[{idx}/{len(match_ids)}] Fetching match {match_id}...", end=" ")

            # Get match details first
            match_info = self.get_match_details(match_id)

            if not match_info:
                print("❌ Failed to get match details")
                continue

            home_team = match_info.get('homeTeam', {}).get('name', 'Unknown')
            away_team = match_info.get('awayTeam', {}).get('name', 'Unknown')
            match_date = datetime.fromtimestamp(match_info.get('startTimestamp', 0)).strftime('%Y-%m-%d')

            print(f"{home_team} vs {away_team} ({match_date})", end=" ")

            # Get lineups
            lineups = self.get_match_lineups(match_id)

            if lineups is None:
                print("- ⏸️  Skipped (no lineup data)")
                self.skipped_matches.append({
                    'match_id': match_id,
                    'date': match_date,
                    'home_team': home_team,
                    'away_team': away_team,
                    'reason': 'No lineup data (404)'
                })
            elif not lineups:
                print("- ❌ Error fetching lineups")
            else:
                player_data = self.extract_player_minutes(lineups, match_info)
                if player_data:
                    self.player_minutes.extend(player_data)
                    print(f"- ✅ OK ({len(player_data)} player records)")
                else:
                    print("- ⚠️  No player data extracted")

            time.sleep(0.5)  # Be respectful to the API

        print("\n" + "=" * 70)
        print(f"Total matches processed: {len(match_ids)}")
        print(f"Total player records extracted: {len(self.player_minutes)}")
        print(f"Total matches skipped (no lineup data): {len(self.skipped_matches)}")
        print(f"Total unique players: {len(self.players_master)}")
        print("=" * 70)

        if self.skipped_matches:
            print(f"\n⏸️  SKIPPED MATCHES ({len(self.skipped_matches)} total):")
            print("-" * 70)
            for match in self.skipped_matches:
                print(f"  {match['date']}: {match['home_team']} vs {match['away_team']}")
                print(f"    Match ID: {match['match_id']} - {match['reason']}")
            print("-" * 70)

    def fetch_player_master_data(self):
        """Fetch detailed information for all unique players."""
        print("\n" + "=" * 70)
        print("Fetching player details for master table...")
        print(f"Total unique players: {len(self.players_master)}")
        print("=" * 70)

        player_details_list = []

        for idx, (player_id, player_name) in enumerate(self.players_master.items(), 1):
            print(f"[{idx}/{len(self.players_master)}] Fetching details for: {player_name}")
            details = self.get_player_details(player_id)

            if details:
                player_details_list.append(details)

            time.sleep(0.5)  # Be respectful to the API

        print(f"Successfully fetched details for {len(player_details_list)} players")
        return player_details_list

    def save_to_csv(self, filename: str = "serie_a_2025_player_minutes.csv"):
        """Save player minutes data to CSV file."""
        if not self.player_minutes:
            print("No data to save!")
            return

        fieldnames = [
            'match_id', 'match_date', 'competition', 'competition_category',
            'team', 'opponent', 'home_away', 'score', 'result',
            'player_id', 'player_name', 'position', 'minutes_played',
            'substitute', 'shirt_number'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.player_minutes)

        print(f"\n✅ Match data saved to {filename}")

    def save_to_json(self, filename: str = "serie_a_2025_player_minutes.json"):
        """Save player minutes data to JSON file."""
        if not self.player_minutes:
            print("No data to save!")
            return

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.player_minutes, jsonfile, indent=2, ensure_ascii=False)

        print(f"✅ Match data saved to {filename}")

    def save_players_master_to_csv(self, player_details: List[Dict], filename: str = "serie_a_2025_players_master.csv"):
        """Save player master data to CSV file."""
        if not player_details:
            print("No player master data to save!")
            return

        fieldnames = [
            'player_id', 'player_name', 'age', 'height', 'weight',
            'nationality', 'position', 'preferred_foot', 'market_value'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(player_details)

        print(f"✅ Player master data saved to {filename}")

    def save_players_master_to_json(self, player_details: List[Dict], filename: str = "serie_a_2025_players_master.json"):
        """Save player master data to JSON file."""
        if not player_details:
            print("No player master data to save!")
            return

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(player_details, jsonfile, indent=2, ensure_ascii=False)

        print(f"✅ Player master data saved to {filename}")


def main():
    """Main execution function."""
    fetcher = DirectMatchFetcher()

    # Fetch all matches by ID
    fetcher.fetch_all_matches(MATCH_IDS)

    # Save match data to both CSV and JSON
    fetcher.save_to_csv()
    fetcher.save_to_json()

    # Fetch player master data and save
    player_details = fetcher.fetch_player_master_data()
    fetcher.save_players_master_to_csv(player_details)
    fetcher.save_players_master_to_json(player_details)

    print("\n" + "=" * 70)
    print("✅ Crawler finished successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
