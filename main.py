import requests
import json
import csv
from datetime import datetime
import time
from typing import List, Dict
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


class CruzeiroCrawler:
    """
    Crawler to fetch Cruzeiro match data from Sofascore API.
    Retrieves all matches from 2025 and extracts minutes played by each player.
    """

    def __init__(self):
        self.base_url = "https://api.sofascore.com/api/v1"
        self.team_id = 1954  # Cruzeiro's team ID
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        self.matches_data = []
        self.player_minutes = []
        self.players_master = {}  # Dictionary to store unique player details

    def get_team_matches(self, page: int = 0) -> List[Dict]:
        """
        Fetch matches for Cruzeiro from Sofascore API.

        Args:
            page: Page number for pagination (default: 0)

        Returns:
            List of match events
        """
        url = f"{self.base_url}/team/{self.team_id}/events/last/{page}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json().get('events', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching matches (page {page}): {e}")
            return []

    def get_match_lineups(self, match_id: int) -> Dict:
        """
        Fetch lineups for a specific match.

        Args:
            match_id: The match event ID

        Returns:
            Dictionary containing lineup data
        """
        url = f"{self.base_url}/event/{match_id}/lineups"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching lineups for match {match_id}: {e}")
            return {}

    def get_player_details(self, player_id: int) -> Dict:
        """
        Fetch detailed information for a specific player.

        Args:
            player_id: The player ID

        Returns:
            Dictionary containing player details
        """
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
                'height': player.get('height'),  # in cm
                'weight': player.get('weight'),  # in kg
                'nationality': player.get('country', {}).get('name', ''),
                'position': player.get('position', ''),
                'preferred_foot': player.get('preferredFoot', ''),
                'market_value': None  # Sofascore doesn't provide this directly
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching player details for player {player_id}: {e}")
            return {}

    def is_match_in_2025(self, match: Dict) -> bool:
        """
        Check if a match was played in 2025.

        Args:
            match: Match dictionary from API

        Returns:
            True if match is in 2025, False otherwise
        """
        if 'startTimestamp' in match:
            match_date = datetime.fromtimestamp(match['startTimestamp'])
            return match_date.year == 2025
        return False

    def extract_player_minutes(self, lineups: Dict, match_info: Dict) -> List[Dict]:
        """
        Extract minutes played by each player from lineup data.

        Args:
            lineups: Lineup data from API
            match_info: Match information (teams, date, etc.)

        Returns:
            List of dictionaries containing player minutes data
        """
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
        if home_team == 'Cruzeiro' or match_info.get('homeTeam', {}).get('id') == self.team_id:
            cruzeiro_side = 'home'
            opponent = away_team
            result = 'W' if home_score > away_score else ('D' if home_score == away_score else 'L')
        elif away_team == 'Cruzeiro' or match_info.get('awayTeam', {}).get('id') == self.team_id:
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
                player_id = player_info.get('id')
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

    def crawl_2025_matches(self):
        """
        Main crawler method to fetch all 2025 matches and extract player minutes.
        """
        print("Starting Cruzeiro 2025 matches crawler...")
        print(f"Team ID: {self.team_id}")
        print("-" * 60)

        all_matches = []
        page = 0
        found_2025_matches = False

        # Fetch matches page by page until we've covered all 2025 matches
        while True:
            print(f"Fetching matches page {page}...")
            matches = self.get_team_matches(page)

            if not matches:
                print("No more matches found.")
                break

            # Filter matches from 2025
            matches_2025 = [m for m in matches if self.is_match_in_2025(m)]

            if matches_2025:
                found_2025_matches = True
                all_matches.extend(matches_2025)
                print(f"Found {len(matches_2025)} matches from 2025 on this page")

            # Check if we've gone past 2025 (into 2024 or earlier)
            if found_2025_matches and not matches_2025:
                # Check if any match is before 2025
                any_before_2025 = any(
                    datetime.fromtimestamp(m.get('startTimestamp', 0)).year < 2025
                    for m in matches
                )
                if any_before_2025:
                    print("Reached matches before 2025, stopping pagination.")
                    break

            page += 1
            time.sleep(0.5)  # Be respectful to the API

            # Safety limit
            if page > 10:
                print("Reached page limit (10), stopping.")
                break

        print(f"\nTotal matches from 2025: {len(all_matches)}")
        print("-" * 60)

        # Process each match to get player minutes
        for idx, match in enumerate(all_matches, 1):
            match_id = match.get('id')
            match_date = datetime.fromtimestamp(match.get('startTimestamp', 0)).strftime('%Y-%m-%d')
            home_team = match.get('homeTeam', {}).get('name', 'Unknown')
            away_team = match.get('awayTeam', {}).get('name', 'Unknown')

            print(f"Processing match {idx}/{len(all_matches)}: {home_team} vs {away_team} ({match_date})")

            lineups = self.get_match_lineups(match_id)
            player_data = self.extract_player_minutes(lineups, match)
            self.player_minutes.extend(player_data)

            time.sleep(0.5)  # Be respectful to the API

        print("-" * 60)
        print(f"Total player records extracted: {len(self.player_minutes)}")

    def fetch_player_master_data(self):
        """
        Fetch detailed information for all unique players.
        """
        print("\n" + "-" * 60)
        print("Fetching player details for master table...")
        print(f"Total unique players: {len(self.players_master)}")
        print("-" * 60)

        player_details_list = []

        for idx, (player_id, player_name) in enumerate(self.players_master.items(), 1):
            print(f"Fetching details for player {idx}/{len(self.players_master)}: {player_name}")
            details = self.get_player_details(player_id)

            if details:
                player_details_list.append(details)

            time.sleep(0.5)  # Be respectful to the API

        print(f"Successfully fetched details for {len(player_details_list)} players")
        return player_details_list

    def save_to_csv(self, filename: str = "cruzeiro_2025_player_minutes.csv"):
        """
        Save player minutes data to CSV file.

        Args:
            filename: Output CSV filename
        """
        if not self.player_minutes:
            print("No data to save!")
            return

        fieldnames = [
            'match_id', 'match_date', 'competition', 'competition_category',
            'opponent', 'home_away', 'score', 'result',
            'player_id', 'player_name', 'position', 'minutes_played',
            'substitute', 'shirt_number'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.player_minutes)

        print(f"Data saved to {filename}")

    def save_to_json(self, filename: str = "cruzeiro_2025_player_minutes.json"):
        """
        Save player minutes data to JSON file.

        Args:
            filename: Output JSON filename
        """
        if not self.player_minutes:
            print("No data to save!")
            return

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.player_minutes, jsonfile, indent=2, ensure_ascii=False)

        print(f"Data saved to {filename}")

    def save_players_master_to_csv(self, player_details: List[Dict], filename: str = "cruzeiro_2025_players_master.csv"):
        """
        Save player master data to CSV file.

        Args:
            player_details: List of player detail dictionaries
            filename: Output CSV filename
        """
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

        print(f"Player master data saved to {filename}")

    def save_players_master_to_json(self, player_details: List[Dict], filename: str = "cruzeiro_2025_players_master.json"):
        """
        Save player master data to JSON file.

        Args:
            player_details: List of player detail dictionaries
            filename: Output JSON filename
        """
        if not player_details:
            print("No player master data to save!")
            return

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(player_details, jsonfile, indent=2, ensure_ascii=False)

        print(f"Player master data saved to {filename}")

    def print_summary(self):
        """Print a summary of the collected data."""
        if not self.player_minutes:
            print("No data collected!")
            return

        print("\n" + "=" * 60)
        print("DATA SUMMARY")
        print("=" * 60)

        # Count unique players
        unique_players = set(p['player_name'] for p in self.player_minutes if p['player_name'])
        print(f"Total unique players: {len(unique_players)}")

        # Count unique matches
        unique_matches = set(p['match_id'] for p in self.player_minutes)
        print(f"Total matches: {len(unique_matches)}")

        # Total minutes by player
        player_total_minutes = {}
        for record in self.player_minutes:
            name = record['player_name']
            minutes = record['minutes_played']
            player_total_minutes[name] = player_total_minutes.get(name, 0) + minutes

        print(f"\nTop 10 players by total minutes played:")
        sorted_players = sorted(player_total_minutes.items(), key=lambda x: x[1], reverse=True)
        for idx, (player, minutes) in enumerate(sorted_players[:10], 1):
            print(f"{idx:2d}. {player:30s} - {minutes:4d} minutes")

        print("=" * 60)


def main():
    """Main execution function."""
    crawler = CruzeiroCrawler()

    # Crawl all 2025 matches
    crawler.crawl_2025_matches()

    # Print summary
    crawler.print_summary()

    # Save match data to both CSV and JSON
    crawler.save_to_csv()
    crawler.save_to_json()

    # Fetch player master data and save
    player_details = crawler.fetch_player_master_data()
    crawler.save_players_master_to_csv(player_details)
    crawler.save_players_master_to_json(player_details)

    print("\nCrawler finished successfully!")


if __name__ == "__main__":
    main()
