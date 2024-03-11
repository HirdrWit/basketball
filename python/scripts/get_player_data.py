import time
import requests
from bs4 import BeautifulSoup
import csv
import re


def parse_team_name(input_string: str) -> str:
    # Define regex pattern
    pattern = r'-(\w+)-'
    # Find all matches
    matches = re.findall(pattern, input_string)
    # Extract the desired match
    if matches:
        return matches[0]
    return "NO_TEAM_NAME"


def get_teams(tables):
    teams = []
    for table in tables:
        # Find the team name
        if "game-basic" not in table.attrs['id']:
            continue
        team_name = parse_team_name(table.attrs['id'])
        if team_name not in teams:
            teams.append(team_name)
    return {teams[0]: teams[1], teams[1]: teams[0]}


def get_game_urls():
    urls = []
    # URL of the webpage
    base_url = "https://www.basketball-reference.com/leagues/NBA_2024_games-{}.html"
    months = ["october", "november", "december", "january", "february", "march", "april"]

    for month in months:
        time.sleep(1)
        url = base_url.format(month)
        print("get_urls: " + url)
        # Send a GET request to the URL
        response = requests.get(url)
        print("response code: " + str(response.status_code))

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the links to box scores
        box_score_links = []
        for link in soup.find_all('a', href=True):
            if 'boxscores' in link['href']:
                box_score_links.append(link['href'])
        # Print the box score links
        for box_score_link in box_score_links:
            if "html" not in box_score_link:
                continue
            urls.append("https://www.basketball-reference.com" + box_score_link)
    return urls


def get_game_results(urls):
    game_results = []
    for url in urls:
        time.sleep(2)
        print("get_urls: " + url)
        # Send a GET request to the URL
        response = requests.get(url)
        print("response code: " + str(response.status_code))
        if response.status_code != 200:
            time.sleep(10)
            print("get_urls: " + url)
            response = requests.get(url)
            print("response code: " + str(response.status_code))
            if response.status_code != 200:
                print("skipping")
                continue

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the tables containing the basic box score stats for both teams
        tables = soup.find_all("table", class_="stats_table")
        opponent = get_teams(tables)
        for table in tables:
            # Find the team name
            if "game-basic" not in table.attrs['id']:
                continue
            team_name = parse_team_name(table.attrs['id'])
            # Find the rows containing the player stats
            player_rows = table.find("tbody").find_all("tr")
            # Iterate over the player rows and extract the stats
            for player_row in player_rows:
                try:
                    player_name = player_row.find("a").text
                    player_stats = [td.text.strip() if len(td.text.strip()) > 0 else '0' for td in
                                    player_row.find_all("td")]
                    if "Did Not Play" in player_stats:
                        continue
                    game_results.append([team_name] + [opponent[team_name]] + [player_name] + player_stats)
                except:
                    continue
    return game_results


def write_results_to_file(results):
    with open("../data/basic_box_score_stats.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(
            ["Team", "Opponent", "Player", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB",
             "DRB",
             "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "+/-"])
        # Write data
        writer.writerows(results)
    print("Data has been scraped and saved to basic_box_score_stats.csv")


# This script retrieves the box score data for every game in the 2024 season from this website
# https://www.basketball-reference.com/leagues/NBA_2024_games.html
def main():
    # Step 1: Get Game URLs
    print("Retrieving Game URLs...")
    game_urls = get_game_urls()
    print("Retrieved " + str(len(game_urls)) + " game URLs.")

    # Step 2: Get Game Data
    print("Retrieving Game Results...")
    game_results = get_game_results(game_urls)

    # Step 3: Write Results to File
    write_results_to_file(game_results)


if __name__ == "__main__":
    main()
