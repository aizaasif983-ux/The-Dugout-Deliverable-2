from dugout.errors import InvalidTeamError, PlayerNotFoundError
from dugout.loader import load_players, read_team_rows, team_from_row


def report(team_name, problems):
    if not problems:
        print(f"{team_name}: LEGAL")
        return

    print(f"{team_name}: REJECTED")
    for problem in problems:
        print(f"- {problem}")


def report_on_row(row, players):
    try:
        team = team_from_row(row, players)
        team.validate()
    except PlayerNotFoundError as error:
        report(row["team_name"], [str(error)])
    except InvalidTeamError as error:
        report(error.team_name, error.problems)
    else:
        report(team.team_name, [])


def main():
    players = load_players("data/players.csv")

    print("The Dugout Fantasy Cricket League")

    for row in read_team_rows("data/bad_teams.csv"):
        report_on_row(row, players)

    print("Team checking completed.")


if __name__ == "__main__":
    main()
