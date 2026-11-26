class InvalidTeamError(Exception):
    def __init__(self, problems):
        self.problems = problems
        super().__init__("Invalid fantasy team")


class PlayerNotFoundError(Exception):
    def __init__(self, player_id):
        self.player_id = player_id
        super().__init__(f"Player {player_id} not found")
