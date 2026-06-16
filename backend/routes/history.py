from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_current_user, get_db_connection
import json

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/")
def get_history(current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, query, result, created_at 
            FROM query_history 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (current_user["id"],))
        rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "query": row[1],
                "result": row[2],
                "created_at": row[3]
            }
            for row in rows
        ]
    finally:
        cur.close()
        conn.close()