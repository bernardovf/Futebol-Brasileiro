"""
Serie A 2025 Crawler for Sofascore Data

IMPORTANT: Team IDs must be verified manually!
-------------------------------------------
Some team IDs in this script need verification. If you see incorrect matches
(e.g., teams from other countries), verify the team ID by:

1. Go to https://www.sofascore.com
2. Search for the team name
3. Check the URL: sofascore.com/team/football/{TEAM_NAME}/{TEAM_ID}
4. Use the TEAM_ID from the URL

Wrong IDs will pull data from teams in other countries with similar names!
"""

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


# Serie A 2025 Teams (18 teams confirmed from user + 2 to be identified)
# Based on 2025 Brasileirão Betano final standings
# IDs verified from sofascore.com team pages
SERIE_A_TEAMS = {
    # VERIFIED IDs
    'Flamengo': 5981,           # ✅ Verified: https://www.sofascore.com/football/team/flamengo/5981
    'Palmeiras': 1963,          # ✅ Verified: https://sofascore.com/team/football/palmeiras/1963
    'Cruzeiro': 1954,           # ✅ Verified (already correct)
    'Mirassol': 21982,          # ✅ Verified: https://www.sofascore.com/football/team/mirassol/21982
    'Botafogo': 1958,           # ✅ Verified: https://www.sofascore.com/team/football/botafogo/1958
    'Bahia': 1955,              # ✅ Verified: https://www.sofascore.com/team/football/bahia/1955
    'Corinthians': 1957,        # ✅ Verified: https://sofascore.com/team/football/corinthians/1957
    'Vasco da Gama': 1974,      # ✅ Verified: https://www.sofascore.com/team/football/vasco-da-gama/1974
    'Ceará': 2001,              # ✅ Verified: https://www.sofascore.com/football/team/ceara/2001
    'Fortaleza': 2020,          # ✅ Verified: https://www.sofascore.com/team/football/fortaleza/2020
    'Sport': 1959,              # ✅ Verified: https://www.sofascore.com/football/team/sport-recife/1959
    'Grêmio': 5926,             # ✅ Verified: https://www.sofascore.com/football/team/gremio/5926
    'Santos': 1968,             # ✅ Verified: https://www.sofascore.com/football/team/santos/1968

    # NEEDS VERIFICATION
    'Fluminense': 1956,         # ⚠️ To verify
    'São Paulo': 1951,          # ⚠️ To verify
    'RB Bragantino': 13354,     # ⚠️ To verify
    'Atlético Mineiro': 1950,   # ⚠️ To verify
    'Juventude': 1963,          # ⚠️ To verify (might conflict with Palmeiras)

    # Missing 2 teams from the 20-team list - please verify against official standings
}


class SerieACrawler:
    """
    Crawler to fetch Serie A match data from Sofascore API.
    Retrieves all Serie A matches from 2025 for all 20 teams.
    """

    def __init__(self, teams: Dict[str, int] = None):
        self.base_url = "https://api.sofascore.com/api/v1"
        self.teams = teams or SERIE_A_TEAMS
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        self.player_minutes = []
        self.players_master = {}  # Dictionary to store unique player details
        self.processed_matches = set()  # Track processed matches to avoid duplicates

    def get_team_matches(self, team_id: int, page: int = 0) -> List[Dict]:
        """
        Fetch matches for a team from Sofascore API.

        Args:
            team_id: The team ID
            page: Page number for pagination (default: 0)

        Returns:
            List of match events
        """
        url = f"{self.base_url}/team/{team_id}/events/last/{page}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json().get('events', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching matches for team {team_id} (page {page}): {e}")
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

    def is_serie_a_match(self, match: Dict) -> bool:
        """
        Check if a match is from Brasileirão Betano (Serie A).

        Args:
            match: Match dictionary from API

        Returns:
            True if match is from Brasileirão Betano, False otherwise
        """
        tournament = match.get('tournament', {})
        tournament_name = tournament.get('name', '').lower()
        tournament_slug = tournament.get('slug', '').lower()

        # Check specifically for Brasileirão Betano (Serie A) - exclude state championships
        # Must contain "brasileiro" or "brasileirão" AND "betano" or be slug "brasileirao"
        is_brasileiro = ('brasileiro' in tournament_name or 'brasileirão' in tournament_name or
                        'brasileirao' in tournament_name or tournament_slug == 'brasileirao')

        # Exclude state championships and other competitions
        exclude_keywords = ['paulista', 'carioca', 'mineiro', 'gaucho', 'pernambucano',
                          'baiano', 'cearense', 'copa', 'serie b', 'série b']

        is_excluded = any(keyword in tournament_name for keyword in exclude_keywords)

        return is_brasileiro and not is_excluded

    def extract_player_minutes(self, lineups: Dict, match_info: Dict, team_id: int) -> List[Dict]:
        """
        Extract minutes played by each player from lineup data.

        Args:
            lineups: Lineup data from API
            match_info: Match information (teams, date, etc.)
            team_id: The team ID we're collecting data for

        Returns:
            List of dictionaries containing player minutes data
        """
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

        # Determine if our team was home or away
        team_side = None
        if match_info.get('homeTeam', {}).get('id') == team_id:
            team_side = 'home'
            team_name = home_team
            opponent = away_team
            result = 'W' if home_score > away_score else ('D' if home_score == away_score else 'L')
        elif match_info.get('awayTeam', {}).get('id') == team_id:
            team_side = 'away'
            team_name = away_team
            opponent = home_team
            result = 'W' if away_score > home_score else ('D' if home_score == away_score else 'L')

        if not team_side:
            return players_data

        # Get team's lineup
        team_lineup = lineups.get(team_side, {})

        # Extract players from starting XI
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
                    'home_away': team_side.upper(),
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

    def crawl_serie_a_2025(self):
        """
        Main crawler method to fetch all Serie A 2025 matches for all teams.
        """
        print("Starting Serie A 2025 crawler...")
        print(f"Total teams: {len(self.teams)}")
        print("=" * 70)

        for team_name, team_id in self.teams.items():
            print(f"\nProcessing team: {team_name} (ID: {team_id})")
            print("-" * 70)

            page = 0
            team_serie_a_matches = 0

            while True:
                matches = self.get_team_matches(team_id, page)

                if not matches:
                    break

                # Filter matches from 2025 and Serie A
                for match in matches:
                    match_id = match.get('id')

                    # Skip if already processed (to avoid duplicates when both teams are in Serie A)
                    if match_id in self.processed_matches:
                        continue

                    if self.is_match_in_2025(match) and self.is_serie_a_match(match):
                        team_serie_a_matches += 1
                        self.processed_matches.add(match_id)

                        match_date = datetime.fromtimestamp(match.get('startTimestamp', 0)).strftime('%Y-%m-%d')
                        home_team = match.get('homeTeam', {}).get('name', 'Unknown')
                        away_team = match.get('awayTeam', {}).get('name', 'Unknown')

                        print(f"  Match {team_serie_a_matches}: {home_team} vs {away_team} ({match_date})")

                        lineups = self.get_match_lineups(match_id)
                        player_data = self.extract_player_minutes(lineups, match, team_id)
                        self.player_minutes.extend(player_data)

                        time.sleep(0.5)  # Be respectful to the API

                # Check if we've gone past 2025
                if any(datetime.fromtimestamp(m.get('startTimestamp', 0)).year < 2025 for m in matches):
                    break

                page += 1
                time.sleep(0.5)

                # Safety limit
                if page > 10:
                    break

            print(f"Total Serie A matches found for {team_name}: {team_serie_a_matches}")

        print("\n" + "=" * 70)
        print(f"Total unique matches processed: {len(self.processed_matches)}")
        print(f"Total player records extracted: {len(self.player_minutes)}")
        print("=" * 70)

        # Verify match count (should be 380 for full Serie A season: 20 teams × 19 rounds × 2)
        expected_matches = 380
        match_count = len(self.processed_matches)
        if match_count < expected_matches:
            print(f"\n⚠️  WARNING: Expected ~{expected_matches} matches for full Serie A season")
            print(f"   Only {match_count} matches found ({expected_matches - match_count} missing)")
            print(f"   This might indicate:")
            print(f"   - Season not yet complete")
            print(f"   - Incorrect team IDs")
            print(f"   - Matches not yet in Sofascore database")
        elif match_count >= expected_matches:
            print(f"\n✅ Successfully collected all {match_count} Serie A matches!")
        print("=" * 70)

    def fetch_player_master_data(self):
        """
        Fetch detailed information for all unique players.
        """
        print("\n" + "=" * 70)
        print("Fetching player details for master table...")
        print(f"Total unique players: {len(self.players_master)}")
        print("=" * 70)

        player_details_list = []

        for idx, (player_id, player_name) in enumerate(self.players_master.items(), 1):
            print(f"Fetching details for player {idx}/{len(self.players_master)}: {player_name}")
            details = self.get_player_details(player_id)

            if details:
                player_details_list.append(details)

            time.sleep(0.5)  # Be respectful to the API

        print(f"Successfully fetched details for {len(player_details_list)} players")
        return player_details_list

    def save_to_csv(self, filename: str = "serie_a_2025_player_minutes.csv"):
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
            'team', 'opponent', 'home_away', 'score', 'result',
            'player_id', 'player_name', 'position', 'minutes_played',
            'substitute', 'shirt_number'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.player_minutes)

        print(f"Match data saved to {filename}")

    def save_to_json(self, filename: str = "serie_a_2025_player_minutes.json"):
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

        print(f"Match data saved to {filename}")

    def save_players_master_to_csv(self, player_details: List[Dict], filename: str = "serie_a_2025_players_master.csv"):
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

    def save_players_master_to_json(self, player_details: List[Dict], filename: str = "serie_a_2025_players_master.json"):
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

        print("\n" + "=" * 70)
        print("DATA SUMMARY")
        print("=" * 70)

        # Count unique players
        unique_players = set(p['player_name'] for p in self.player_minutes if p['player_name'])
        print(f"Total unique players: {len(unique_players)}")

        # Count unique matches
        print(f"Total unique matches: {len(self.processed_matches)}")

        # Count by team
        team_counts = {}
        for record in self.player_minutes:
            team = record['team']
            team_counts[team] = team_counts.get(team, 0) + 1

        print(f"\nPlayer records by team:")
        for team, count in sorted(team_counts.items()):
            print(f"  {team:30s}: {count:4d} records")

        # Total minutes by player
        player_total_minutes = {}
        for record in self.player_minutes:
            name = record['player_name']
            minutes = record['minutes_played']
            player_total_minutes[name] = player_total_minutes.get(name, 0) + minutes

        print(f"\nTop 15 players by total minutes played:")
        sorted_players = sorted(player_total_minutes.items(), key=lambda x: x[1], reverse=True)
        for idx, (player, minutes) in enumerate(sorted_players[:15], 1):
            print(f"{idx:2d}. {player:35s} - {minutes:5d} minutes")

        print("=" * 70)


def main():
    """Main execution function."""
    crawler = SerieACrawler()

    # Crawl all Serie A 2025 matches
    crawler.crawl_serie_a_2025()

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
