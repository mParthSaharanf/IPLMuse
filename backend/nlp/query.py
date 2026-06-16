from nlp.extractor import extract_query_params
from nlp.query_builder import build_and_execute
from nlp.player_cache import ALL_PLAYERS
from nlp.compute import compute_metric  

class QueryProcessor:
    def __init__(self, raw_query: str):
        self.raw_query = raw_query
        self.params = None
        self.db_result = None
        self.result = None

    def extract(self):
        self.params = extract_query_params(self.raw_query)
        return self
    
    def query_db(self, cur, all_players):
        if self.params is None:
            raise ValueError("Parameters not extracted yet")
        self.db_result = build_and_execute(self.params, cur, all_players)
        return self
    
    def compute(self):
        if self.db_result is None:
            raise ValueError("Database query not executed yet")
        self.result = compute_metric(self.params['metric'], self.db_result)
        return self
