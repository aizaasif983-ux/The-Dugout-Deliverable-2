import csv
import json
from pathlib import Path
from dugout.models import Player, FantasyTeam


def load_players(filename):
    players = {}
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            player = Player.from_row(row)
            players[player.player_id] = player
    return players


def load_teams_json(filename, players):
    if not Path(filename).exists():
        return []

    with open(filename, encoding="utf-8") as file:
        data = json.load(file)

    return [
        FantasyTeam.from_dict(item, players)
        for item in data
    ]


def save_teams_json(filename, teams):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            [team.to_dict() for team in teams],
            file,
            indent=4
        )
