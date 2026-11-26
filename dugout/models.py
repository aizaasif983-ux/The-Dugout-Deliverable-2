from dugout.rules import (
    check_players_count,
    check_budget,
    check_franchise_limit,
    check_roles,
    check_captains,
    check_no_duplicates,
)
from dugout.errors import InvalidTeamError, PlayerNotFoundError


class Player:
    def __init__(self, player_id, name, franchise, role, credits):
        self.player_id = player_id
        self.name = name
        self.franchise = franchise
        self.role = role
        self.credits = credits

    @classmethod
    def from_row(cls, row):
        return cls(
            row["player_id"],
            row["name"],
            row["franchise"],
            row["role"],
            float(row["credits"])
        )

    def __str__(self):
        return f"{self.name} ({self.franchise}, {self.role}, {self.credits} cr)"


class FantasyTeam:
    def __init__(self, team_name, owner):
        self.team_name = team_name
        self.owner = owner
        self.players = []
        self.captain = None
        self.vice_captain = None

    def add_player(self, player):
        self.players.append(player)

    def total_credits(self):
        return sum(player.credits for player in self.players)

    def count_by_role(self):
        counts = {"WK": 0, "BAT": 0, "AR": 0, "BOWL": 0}
        for player in self.players:
            counts[player.role] += 1
        return counts

    def set_captain(self, captain, vice_captain):
        self.captain = captain
        self.vice_captain = vice_captain

    def count_by_franchise(self):
        counts = {}
        for player in self.players:
            counts[player.franchise] = counts.get(player.franchise, 0) + 1
        return counts

    def check_rules(self):
        errors = []
        errors.extend(check_players_count(self))
        errors.extend(check_budget(self))
        errors.extend(check_franchise_limit(self))
        errors.extend(check_roles(self))
        errors.extend(check_captains(self))
        errors.extend(check_no_duplicates(self))
        return errors

    def validate(self):
        problems = self.check_rules()
        if problems:
            raise InvalidTeamError(problems)

    def to_dict(self):
        return {
            "team_name": self.team_name,
            "owner": self.owner,
            "player_ids": [p.player_id for p in self.players],
            "captain": self.captain.player_id if self.captain else None,
            "vice_captain": self.vice_captain.player_id if self.vice_captain else None
        }

    @classmethod
    def from_dict(cls, data, players):
        team = cls(data["team_name"], data["owner"])

        def find_player(player_id):
            if player_id not in players:
                raise PlayerNotFoundError(player_id)
            return players[player_id]

        for player_id in data["player_ids"]:
            team.add_player(find_player(player_id))

        team.set_captain(
            find_player(data["captain"]),
            find_player(data["vice_captain"])
        )
        return team

    def __str__(self):
        return f"{self.team_name} (owner: {self.owner})"


class League:
    def __init__(self, name):
        self.name = name
        self.teams = {}

    def add_team(self, team):
        self.teams[team.owner] = team

    def find_team(self, owner):
        return self.teams.get(owner)

    def legal_teams(self):
        return [team for team in self.teams.values() if not team.check_rules()]

    def rank_teams(self):
        return sorted(self.teams.values(), key=lambda team: team.total_credits())
