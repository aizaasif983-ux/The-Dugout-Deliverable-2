from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from dugout.models import FantasyTeam
from dugout.errors import InvalidTeamError, PlayerNotFoundError
from dugout.loader import load_players, load_teams_json, save_teams_json

app = FastAPI(title="The Dugout API")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PLAYERS_CSV = DATA_DIR / "players.csv"
TEAMS_JSON = DATA_DIR / "teams.json"

players = load_players(PLAYERS_CSV)
teams = {
    i: team
    for i, team in enumerate(
        load_teams_json(TEAMS_JSON, players), start=1
    )
}


class TeamIn(BaseModel):
    team_name: str = Field(min_length=1, max_length=40)
    owner: str = Field(min_length=1, max_length=40)
    player_ids: list[str]
    captain: str
    vice_captain: str


def next_team_id():
    return max(teams.keys(), default=0) + 1


def team_details(team_id, team):
    return {
        "team_id": team_id,
        "team_name": team.team_name,
        "owner": team.owner,
        "captain": team.captain.name,
        "vice_captain": team.vice_captain.name,
        "credits_used": team.total_credits(),
        "credits_left": round(100 - team.total_credits(), 2),
        "count_by_role": team.count_by_role()
    }


@app.get("/")
def home():
    return {"message": "Welcome to The Dugout"}


@app.get("/players")
def get_players(role: str = None, franchise: str = None):
    result = list(players.values())

    if role:
        result = [p for p in result if p.role == role]

    if franchise:
        result = [p for p in result if p.franchise == franchise]

    return [vars(p) for p in result]


@app.get("/players/{player_id}")
def get_player(player_id: str):
    if player_id not in players:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )
    return vars(players[player_id])


@app.get("/teams")
def get_teams():
    return [
        team_details(team_id, team)
        for team_id, team in teams.items()
    ]


@app.get("/teams/{team_id}")
def get_team(team_id: int):
    if team_id not in teams:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    return team_details(team_id, teams[team_id])


@app.post("/teams", status_code=201)
def register_team(team_in: TeamIn):
    try:
        team = FantasyTeam.from_dict(
            team_in.model_dump(), players
        )
    except PlayerNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    try:
        team.validate()
    except InvalidTeamError as error:
        raise HTTPException(
            status_code=400,
            detail={
                "message": str(error),
                "problems": error.problems
            }
        )

    team_id = next_team_id()
    teams[team_id] = team
    save_teams_json(TEAMS_JSON, list(teams.values()))

    return team_details(team_id, team)
@app.get("/player-count")
def player_count():
    return {"total_players": len(players)}



