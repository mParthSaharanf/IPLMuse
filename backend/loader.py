import json 
import glob
import psycopg2
import os

conn = psycopg2.connect(
    host = 'localhost',
    database = 'ipldb',
    user = 'iplmuse',
    password = '335051'
)

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS matches(
    match_id INTEGER PRIMARY KEY,
    season varchar(10) NOT NULL,
    date DATE NOT NULL,
    venue varchar(100) NOT NULL,
    city varchar(50) NOT NULL,
    team1 varchar(50) NOT NULL,
    team2 varchar(50) NOT NULL,
    toss_winner varchar(50) NOT NULL,
    toss_decision varchar(10) NOT NULL,
    winner varchar(50),
    win_by_runs INTEGER,
    win_by_wickets INTEGER,
    player_of_match varchar(100)                
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS players(
    player_id varchar(50) PRIMARY KEY,
    player_name varchar(100) NOT NULL                  
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS deliveries(
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(match_id),
    inning INTEGER,
    over INTEGER,
    ball INTEGER,
    batter VARCHAR(100),
    bowler VARCHAR(100),
    non_striker VARCHAR(100),
    batter_runs INTEGER,
    extra_runs INTEGER,
    total_runs INTEGER,
    wide INTEGER DEFAULT 0,
    noball INTEGER DEFAULT 0,
    bye INTEGER DEFAULT 0,
    legbye INTEGER DEFAULT 0,
    is_wicket BOOLEAN DEFAULT FALSE,
    wicket_kind VARCHAR(50),
    player_out VARCHAR(100),
    fielder VARCHAR(100)
)''')
conn.commit()

json_files = glob.glob(os.path.join("ipl_json/*.json"))

for file_path in json_files:
    with open(file_path) as f:
        data = json.load(f)
    
    match_id = int(os.path.basename(file_path).replace('.json', ''))
    info = data['info']
    season = info['season']
    date = info['dates'][0]
    venue = info['venue']
    city = info.get('city','')
    team1 = info['teams'][0]
    team2 = info['teams'][1]
    toss_winner = info['toss']['winner']
    toss_decision = info['toss']['decision']
    winner = info['outcome'].get('winner', None)
    win_by_runs = info['outcome'].get('by', {}).get('runs', None)
    win_by_wickets = info['outcome'].get('by', {}).get('wickets', None)
    player_of_match = info.get('player_of_match', [None])[0]

    cur.execute('''INSERT INTO matches VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING''',
        (match_id, season, date, venue, city, team1, team2,
        toss_winner, toss_decision, winner, win_by_runs,
        win_by_wickets, player_of_match))
    
    for name, pid in info['registry']['people'].items():
        cur.execute('''INSERT INTO players VALUES (%s,%s)
            ON CONFLICT DO NOTHING''', (pid, name))
    
    for inning_idx, inning in enumerate(data['innings']):
        for over in inning['overs']:
            for ball_idx, delivery in enumerate(over['deliveries']):
                extras = delivery.get('extras', {})
                wickets = delivery.get('wickets', [])
                is_wicket = len(wickets) > 0
                wicket_kind = wickets[0].get('kind', None) if is_wicket else None
                player_out = wickets[0].get('player_out', None) if is_wicket else None
                fielders = wickets[0].get('fielders', []) if is_wicket else []
                fielder = fielders[0].get('name', None) if fielders else None

                cur.execute('''INSERT INTO deliveries 
                    (match_id, inning, over, ball, batter, bowler,
                    non_striker, batter_runs, extra_runs, total_runs,
                    wide, noball, bye, legbye, is_wicket, wicket_kind,
                    player_out, fielder)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (match_id, inning_idx+1, over['over'], ball_idx,
                    delivery['batter'], delivery['bowler'],
                    delivery['non_striker'],
                    delivery['runs']['batter'],
                    delivery['runs']['extras'],
                    delivery['runs']['total'],
                    extras.get('wides', 0),
                    extras.get('noballs', 0),
                    extras.get('byes', 0),
                    extras.get('legbyes', 0),
                    is_wicket, wicket_kind, player_out, fielder))

conn.commit()
conn.close()