from rapidfuzz import process, fuzz

def resolve_player(name: str, all_players: list) -> str:
    if not name:
        return None
    match = process.extractOne(
        name, 
        all_players,
        scorer=fuzz.WRatio,
        score_cutoff=60
    )
    if match:
        return match[0]
    return name  # return original if no good match found