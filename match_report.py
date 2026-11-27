import sys
from dugout.matches import load_match, deliveries


def main():
    path = "data/matches/match_01.json"

    if len(sys.argv) > 1:
        path = sys.argv[1]

    match = load_match(path)
    info = match["info"]

    print("The Dugout Match Report")
    print("Teams:", " vs ".join(info["teams"]))
    print("Venue:", info["venue"])
    print("Winner:", info["outcome"].get("winner", "No result"))

    totals = {}
    scores = {}

    for team, over, ball in deliveries(match):
        totals[team] = totals.get(team, 0) + ball["runs"]["total"]

        batter = ball["batter"]
        scores[batter] = scores.get(batter, 0) + ball["runs"]["batter"]

    print("\nTeam Scores:")
    for team, runs in totals.items():
        print(team, runs)

    print("\nTop Scorers:")
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for name, runs in ranked[:3]:
        print(name, runs)


if __name__ == "__main__":
    main()
