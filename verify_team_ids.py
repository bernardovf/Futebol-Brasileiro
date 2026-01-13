"""
Script to verify and get correct Sofascore team IDs for Serie A 2025 teams.
Based on search results and manual verification.
"""

# Correct Sofascore Team IDs for Brazilian Serie A 2025
# Verified from sofascore.com URLs

VERIFIED_SERIE_A_TEAMS = {
    # Verified IDs
    'Flamengo': 5981,           # https://www.sofascore.com/football/team/flamengo/5981
    'Palmeiras': 1963,          # https://sofascore.com/team/football/palmeiras/1963
    'Botafogo': 1958,           # https://www.sofascore.com/team/football/botafogo/1958
    'Corinthians': 1957,        # https://sofascore.com/team/football/corinthians/1957
    'São Paulo': 5981,          # Need to verify - placeholder
    'Cruzeiro': 1954,           # Already verified
    'Atlético Mineiro': 1952,   # Need to verify
    'Internacional': 1961,      # Need to verify
    'Fluminense': 1956,         # Need to verify
    'Grêmio': 1955,             # Need to verify
    'Vasco da Gama': 1957,      # Need to verify - might conflict with Corinthians
    'Bahia': 1959,              # Need to verify
    'Fortaleza': 1968,          # Need to verify
    'Athletico Paranaense': 1960, # Need to verify
    'RB Bragantino': 13354,     # Need to verify
    'Santos': 1950,             # Need to verify (promoted)
    'Juventude': 1963,          # Need to verify - might conflict with Palmeiras
    'Vitória': 2020,            # Need to verify
    'Cuiabá': 34911,            # Need to verify
    'Atlético Goianiense': 7314, # https://www.sofascore.com/team/football/atletico-goianiense/7314
}

# Teams from 2025 Serie A (need to verify which 20 are correct)
# Note: Santos, Mirassol, Ceará, and Sport were promoted from Serie B

TEAMS_TO_VERIFY = [
    'Botafogo',
    'Palmeiras',
    'Flamengo',
    'São Paulo',
    'Fortaleza',
    'Internacional',
    'Cruzeiro',
    'Bahia',
    'Corinthians',
    'Atlético Mineiro',
    'Vasco da Gama',
    'Fluminense',
    'Grêmio',
    'Juventude',
    'RB Bragantino',
    'Athletico Paranaense',
    'Vitória',
    'Cuiabá',
    'Atlético Goianiense',
    'Santos'  # Promoted from Serie B
]

print("Verified Team IDs for Serie A 2025:")
print("=" * 70)
for team, team_id in VERIFIED_SERIE_A_TEAMS.items():
    print(f"{team:30s}: {team_id:6d}")
print("=" * 70)
print(f"\nTotal teams: {len(VERIFIED_SERIE_A_TEAMS)}")
print("\nNote: Some IDs need verification. Cross-check with Sofascore website.")
