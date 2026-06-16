import ollama
import json
import os

def extract_query_params(query: str) -> dict:
    prompt = f"""
    You are a Great Cricket stats query parser for IPL data.
    Extract the following fields from the user's question and return ONLY a JSON object, no extra text, no markdown, no backticks.

    Fields to extract:
- player: full name of the player (string or null)
- season: IPL season year like "2023" or "2023/24" (string or null)
- metric: what stat is being asked. one of: total_runs, total_wickets, batting_average, strike_rate, economy_rate, highest_score, 
  total_fours, total_sixes, total_balls_faced,centuries, half_centuries, ducks, bowling_average, bowling_strike_rate, dot_balls,
  runs_conceded, best_bowling_figures, maiden_overs (string or null)
- team: team name if mentioned (string or null)
- phase: powerplay, middle, death (string or null)
- match_range: if a range of matches is mentioned return as [start, end] (array or null)

User's question: {query}

Return only JSON like this:
{{
  "player": "David Warner",
  "season": "2016",
  "metric": "batting_average",
  "team": null,
  "phase": null,
  "match_range": [3, 7]
}}
Important: use JSON null (not the string "null") for missing values
"""
    response = ollama.chat(
        model = "llama3.2:3b",
        messages = [{"role": "user", "content": prompt}]
    )
    try:
        text = response['message']['content'].strip()
        return json.loads(text)
    except json.JSONDecodeError:
        print("Failed to parse JSON:", text)
        return {
            "player": None,
            "season": None,
            "metric": None,
            "team": None,
            "phase": None,
            "match_range": None
        }
    
if __name__ == "__main__":
    result = extract_query_params("how many runs did David Warner score in the 2016 season?")
    print(result)