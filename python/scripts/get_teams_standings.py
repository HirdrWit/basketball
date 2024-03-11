import requests
from bs4 import BeautifulSoup
import re

output_file_path = '../data/team_standings.py'

team_map = {
    "Boston Celtics": "BOS",
    "Cleveland Cavaliers": "CLE",
    "Milwaukee Bucks": "MIL",
    "New York Knicks": "NYK",
    "Philadelphia 76ers": "PHI",
    "Orlando Magic": "ORL",
    "Miami Heat": "MIA",
    "Indiana Pacers": "IND",
    "Chicago Bulls": "CHI",
    "Atlanta Hawks": "ATL",
    "Brooklyn Nets": "BRK",
    "Toronto Raptors": "TOR",
    "Charlotte Hornets": "CHO",
    "Detroit Pistons": "DET",
    "Washington Wizards": "WAS",
    "Minnesota Timberwolves": "MIN",
    "Oklahoma City Thunder": "OKC",
    "Denver Nuggets": "DEN",
    "Los Angeles Clippers": "LAC",
    "Phoenix Suns": "PHO",
    "New Orleans Pelicans": "NOP",
    "Sacramento Kings": "SAC",
    "Dallas Mavericks": "DAK",
    "Golden State Warriors": "GSW",
    "Los Angeles Lakers": "LAL",
    "Utah Jazz": "UTA",
    "Houston Rockets": "HOU",
    "Memphis Grizzlies": "MEM",
    "Portland Trail Blazers": "POR",
    "San Antonio Spurs": "SAS",
}


def get_team_position_int(text):
    # Define the regex pattern to extract the number
    pattern = r'\((\d+)\)'

    # Search for the pattern in the text
    match = re.search(pattern, text)

    if match:
        # Extract the number from the matched group
        number = match.group(1)
        return number
    else:
        print("No number found for {}.", text)


def get_standings(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the standings
    east_table = soup.find('table', {'id': 'confs_standings_E'})
    west_table = soup.find('table', {'id': 'confs_standings_W'})

    # Initialize lists to store team names and positions
    teams = []
    positions = []

    # Iterate over rows in the table
    for row in east_table.find_all('tr')[1:]:
        # Find the team name
        team = row.find('a').text
        teams.append(team_map.get(team))

        # Find the team's position in the bracket
        position = row.find('th').text
        positions.append(get_team_position_int(position))

    for row in west_table.find_all('tr')[1:]:
        # Find the team name
        team = row.find('a').text
        teams.append(team_map.get(team))

        # Find the team's position in the bracket
        position = row.find('th').text
        positions.append(get_team_position_int(position))

    # Return a dictionary with team names as keys and their positions as values
    return dict(zip(teams, positions))


if __name__ == "__main__":
    url = 'https://www.basketball-reference.com/leagues/NBA_2024_standings.html'
    standings = get_standings(url)

    # Write the dictionary to a Python file
    with open(output_file_path, 'w') as py_file:
        py_file.write('def get_dict(): \n')
        py_file.write('\t return ')
        py_file.write(repr(standings))  # Write the representation of the dictionary as Python code

    print("Dictionary written to", output_file_path)
