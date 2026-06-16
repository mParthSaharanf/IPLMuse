from nlp.metrics import (batting_average, strike_rate, economy_rate, 
    highest_score, total_runs, total_wickets, total_fours, total_sixes,
    total_balls_faced, centuries, half_centuries, ducks, bowling_average,
    bowling_strike_rate, dot_balls, runs_conceded, best_bowling_figures, 
    maiden_overs)

def compute_metric(metric: str, data: dict) -> dict:
    if metric == "total_runs":
        return {"total_runs": total_runs(data["runs"])}
    
    elif metric == "total_wickets":
        return {"total_wickets": total_wickets(data["wickets"])}
    
    elif metric == "batting_average":
        return {"batting_average": batting_average(data["runs"], data["dismissals"])}
    
    elif metric == "strike_rate":
        return {"strike_rate": strike_rate(data["runs"], data["balls_faced"])}
    
    elif metric == "economy_rate":
        return {"economy_rate": economy_rate(data["runs_conceded"], data["balls_bowled"])}
    
    elif metric == "highest_score":
        return {"highest_score": highest_score(data["scores"])}
    
    elif metric == "total_fours":
        return {"total_fours": total_fours(data["count"])}
    
    elif metric == "total_sixes":
        return {"total_sixes": total_sixes(data["count"])}
    
    elif metric == "total_balls_faced":
        return {"total_balls_faced": total_balls_faced(data["count"])}
    
    elif metric == "centuries":
        return {"centuries": centuries(data["scores"])}
    
    elif metric == "half_centuries":
        return {"half_centuries": half_centuries(data["scores"])}
    
    elif metric == "ducks":
        return {"ducks": ducks(data["scores"])}
    
    elif metric == "bowling_average":
        return {"bowling_average": bowling_average(data["runs_conceded"], data["wickets"])}
    
    elif metric == "bowling_strike_rate":
        return {"bowling_strike_rate": bowling_strike_rate(data["balls_bowled"], data["wickets"])}
    
    elif metric == "dot_balls":
        return {"dot_balls": dot_balls(data["count"])}
    
    elif metric == "runs_conceded":
        return {"runs_conceded": runs_conceded(data["runs"])}
    
    elif metric == "best_bowling_figures":
        return {"best_bowling_figures": best_bowling_figures(data["figures"])}
    
    elif metric == "maiden_overs":
        return {"maiden_overs": maiden_overs(data["count"])}
    
    else:
        return {"error": "Unknown metric"}