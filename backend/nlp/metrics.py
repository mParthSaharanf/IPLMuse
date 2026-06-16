def batting_average(runs: int, dismissals: int) -> float:
    if dismissals == 0:
        return float(runs)
    return runs / dismissals

def strike_rate(runs:int, balls_faced:int) -> float:
    if balls_faced == 0:
        return 0.0
    return (runs / balls_faced) * 100

def total_fours(count: int) -> int:
    return count

def total_sixes(count: int) -> int:
    return count

def total_balls_faced(count: int) -> int:
    return count

def centuries(scores: list) -> int:
    return sum(1 for score in scores if score >= 100)

def half_centuries(scores: list) -> int:
    return sum(1 for score in scores if 50 <= score < 100)

def ducks(scores: list) -> int:
    return sum(1 for score in scores if score == 0)

def bowling_average(runs_conceded: int, wickets: int) -> float:
    if wickets == 0:
        return 0.0
    return runs_conceded / wickets

def bowling_strike_rate(balls_bowled: int, wickets: int) -> float:
    if wickets == 0:
        return 0.0
    return balls_bowled / wickets

def dot_balls(count: int) -> int:
    return count

def runs_conceded(count: int) -> int:
    return count

def economy_rate(runs_conceded: int, balls_bowled: float) -> float:
    if balls_bowled == 0:
        return 0.0
    return (runs_conceded / balls_bowled) * 6

def highest_score(scores: list) -> int:
    if not scores:
        return 0
    return max(scores)

def total_runs(runs: int) -> int:
    return runs

def total_wickets(wickets: int) -> int:
    return wickets

def best_bowling_figures(figures: list) -> dict:
    if not figures:
        return {"wickets": 0, "runs": 0}
    best = max(figures, key=lambda x: (x[0], -x[1]))
    return {"wickets": best[0], "runs": best[1]}

def maiden_overs(count: int) -> int:
    return count
