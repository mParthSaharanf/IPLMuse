ALL_PLAYERS = []

def load_players(cur):

    cur.execute("""
        SELECT player_name
        FROM players
    """)
    ALL_PLAYERS.clear()

    ALL_PLAYERS.extend(
        row[0]
        for row in cur.fetchall()
    )


    print(
        f"Loaded {len(ALL_PLAYERS)} players"
    )