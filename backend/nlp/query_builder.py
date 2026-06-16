import psycopg2
import logging
from nlp.entity_resolver import resolve_player

def build_and_execute(params: dict, cur, all_players) -> dict:
    print("build_and_execute called with:", params)
    metric = params.get('metric',None)
    season = params.get('season',None)
    player = params.get('player',None)
    team = params.get('team',None)
    phase = params.get('phase',None)
    match_range = params.get('match_range', None)

    if player:
        print("Number of players:", len(all_players))
        print("Original player:", player)
        player = resolve_player(player, all_players)

    filters = ["1=1"]
    values = []

    if metric in ["batting_average", "strike_rate", "total_runs", "highest_score", "total_fours", "total_sixes", "total_balls_faced", "centuries", "half_centuries", "ducks"]:
        filters.append("d.batter = %s")
        values.append(player)
    elif metric in ["economy_rate", "total_wickets", "bowling_average", "bowling_strike_rate", "dot_balls", "runs_conceded","best_bowling_figures","maiden_overs"]:
        filters.append("d.bowler = %s")
        values.append(player)

    if season:
        filters.append("m.season = %s")
        values.append(season)
    
    
    where_clause = " AND ".join(filters)

    logging.debug(f"PARAMS: {params}")
    logging.debug(f"METRIC: {metric}")
    logging.debug(f"WHERE: {where_clause}")
    logging.debug(f"VALUES: {values}")

    if metric == "total_runs":
        cur.execute(f"""
                    SELECT SUM(d.batter_runs)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    """, values)
        result = cur.fetchone()[0]
        return {"runs": result or 0}
    elif metric == "batting_average":
        cur.execute(f"""
                    SELECT SUM(d.batter_runs), SUM(CASE WHEN d.is_wicket THEN 1 ELSE 0 END)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    """, values)
        result = cur.fetchone()
        return {"runs": result[0] or 0, "dismissals": result[1] or 0}
    elif metric == "strike_rate":
        cur.execute(f"""
                    SELECT SUM(d.batter_runs),COUNT(*) FILTER (WHERE d.wide = 0)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    """, values)
        result = cur.fetchone()
        return {"runs": result[0] or 0, "balls_faced": result[1] or 0}
    elif metric == 'total_fours':
        cur.execute(f"""
                    SELECT COUNT(*)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    AND d.batter_runs = 4
                    """, values)
        result = cur.fetchone()[0]
        return {"count": result or 0}

    elif metric == 'total_sixes':
        cur.execute(f"""
                    SELECT COUNT(*)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    AND d.batter_runs = 6
                    """, values)
        result = cur.fetchone()[0]
        return {"count": result or 0}
    
    elif metric == "total_balls_faced":
        cur.execute(f"""
                    SELECT COUNT(*) 
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    AND d.wide = 0
                    """,values)
        result = cur.fetchone()[0]
        return {"count": result or 0}
    
    elif metric == 'centuries':
        cur.execute(f"""
                    SELECT SUM(d.batter_runs)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    GROUP BY d.match_id
                    HAVING SUM(d.batter_runs) >= 100
                    """, values)
        rows = cur.fetchall()
        return {"scores": [row[0] for row in rows]}
    elif metric == 'half_centuries':
        cur.execute(f"""
                    SELECT SUM(d.batter_runs)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    GROUP BY d.match_id
                    HAVING SUM(d.batter_runs) >= 50 AND SUM(d.batter_runs) < 100
                    """, values)
        rows = cur.fetchall()
        return {"scores": [row[0] for row in rows]}
    
    elif metric == 'ducks':
        cur.execute(f"""
                    SELECT COUNT(*) FROM (
                    SELECT d.match_id
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    GROUP BY d.match_id
                    HAVING SUM(d.batter_runs) = 0
                    AND MAX(CASE WHEN d.is_wicket = TRUE AND d.player_out = %s THEN 1 ELSE 0 END) = 1
                    ) subquery
                """, values + [player])
        rows = cur.fetchall()
        return {"scores": [row[0] for row in rows]}

    elif metric == 'dot_balls':
        cur.execute(f"""
                    SELECT COUNT(*)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    AND d.total_runs = 0
                    """, values)
        result = cur.fetchone()[0]
        return {"count": result or 0}
    
    elif metric == 'runs_conceded':
        cur.execute(f"""
                    SELECT SUM(d.total_runs)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    """, values)
        result = cur.fetchone()[0]
        return {"runs": result or 0}

    elif metric == 'bowling_strike_rate':
        cur.execute(f"""
                    SELECT COUNT(*) FILTER (WHERE d.wide = 0 AND d.noball = 0),
                    COUNT(*) FILTER (WHERE d.is_wicket = TRUE AND d.wicket_kind NOT IN ('run out', 'retired hurt', 'obstructing the field'))
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    """, values)
        row = cur.fetchone()
        return {"balls_bowled": row[0] or 0, "wickets": row[1] or 0}

    elif metric == 'bowling_average':
        cur.execute(f"""
                    SELECT SUM(d.total_runs),
                    COUNT(*) FILTER (WHERE d.is_wicket = TRUE AND d.wicket_kind NOT IN ('run out', 'retired hurt', 'obstructing the field'))
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    """, values)
        row = cur.fetchone()
        return {"runs_conceded": row[0] or 0, "wickets": row[1] or 0}
    elif metric == 'economy_rate':
        cur.execute(f"""
                    SELECT SUM(d.total_runs), COUNT(*) FILTER (WHERE d.wide = 0 AND d.noball = 0)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    """, values)
        row = cur.fetchone()
        return {"runs_conceded": row[0] or 0, "balls_bowled": row[1] or 0}

    elif metric == 'total_wickets':
        cur.execute(f"""
                    SELECT COUNT(*) 
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause} AND d.is_wicket = TRUE
                    AND d.wicket_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
                    """, values)
        result = cur.fetchone()[0]
        return {"wickets": result or 0}
    
    elif metric == 'best_bowling_figures':
        cur.execute(f"""
                    SELECT d.match_id,
                    COUNT(*) FILTER (WHERE d.is_wicket = TRUE AND d.wicket_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')),
                    SUM(d.total_runs)
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    GROUP BY d.match_id
                    """, values)
        rows = cur.fetchall()
        figures = [(row[1], row[2]) for row in rows]
        return {"figures": figures}

    elif metric == 'maiden_overs':
        cur.execute(f"""
                    SELECT COUNT(*) FROM (
                    SELECT d.match_id, d.over
                    FROM deliveries d
                    JOIN matches m ON d.match_id = m.match_id
                    WHERE {where_clause}
                    GROUP BY d.match_id, d.over
                    HAVING SUM(d.total_runs) = 0
                    AND COUNT(*) = 6
                    ) subquery
                """, values)
        result = cur.fetchone()[0]
        return {"count": result or 0}

    elif metric == 'highest_score':
        cur.execute(f"""
            SELECT d.match_id, SUM(d.batter_runs)
            FROM deliveries d
            JOIN matches m ON d.match_id = m.match_id
            WHERE {where_clause}
            GROUP BY d.match_id
        """, values)
        rows = cur.fetchall()
        scores = [row[1] for row in rows]
        return {"scores": scores}
    
    return {}