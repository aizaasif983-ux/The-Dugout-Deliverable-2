import json


def load_match(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def deliveries(match):
    for innings in match["innings"]:
        for over in innings["overs"]:
            for ball in over["deliveries"]:
                yield innings["team"], over["over"], ball


def is_ball_faced(delivery):
    extras = delivery.get("extras", {})
    return "wides" not in extras and "noballs" not in extras


def batter_runs(match, batter):
    runs = 0
    for team, over, ball in deliveries(match):
        if ball["batter"] == batter:
            runs += ball["runs"]["batter"]
    return runs
