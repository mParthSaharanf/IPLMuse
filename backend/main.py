from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from nlp.query import QueryProcessor
from nlp.player_cache import ALL_PLAYERS, load_players
from routes.auth import router as auth_router
from routes.history import router as history_router
from routes.favorites import router as favorites_router
from dependencies import get_current_user, get_db_connection
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD


import json
import psycopg2
import logging

logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn, cur = db_connection()
    load_players(cur)
    cur.close()
    conn.close()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(history_router)
app.include_router(favorites_router)

def db_connection():
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        curr = conn.cursor()
        return conn, curr
    except Exception as e:
        print("Error connecting to database:", e)
        return None, None

@app.get("/ask")
def ask_question(q: str, current_user = Depends(get_current_user)):
    conn, cur = db_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    try:
        processor = QueryProcessor(q)
        processor.extract().query_db(cur, ALL_PLAYERS)
        logging.debug(f"DB Result: {processor.db_result}")
        processor.compute()

        # save to history
        hist_conn = get_db_connection()
        hist_cur = hist_conn.cursor()
        try:
            hist_cur.execute("""
                INSERT INTO query_history (user_id, query, result)
                VALUES (%s, %s, %s)
            """, (current_user["id"], q, json.dumps(processor.result)))
            hist_conn.commit()
        finally:
            hist_cur.close()
            hist_conn.close()

        return processor.result
    except Exception as e:
        import traceback
        return {"error": str(e), "detail": traceback.format_exc()}
    finally:
        cur.close()
        conn.close()