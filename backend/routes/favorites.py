from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_current_user, get_db_connection
from pydantic import BaseModel
import json

router = APIRouter(prefix="/favorites", tags=["favorites"])

class FavoriteRequest(BaseModel):
    query: str
    result: dict
    label: str = None

@router.post("/")
def add_favorite(req: FavoriteRequest, current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO favorites (user_id, query, result, label)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, query) DO NOTHING
            RETURNING id
        """, (current_user["id"], req.query, json.dumps(req.result), req.label))
        conn.commit()
        return {"message": "Added to favorites"}
    finally:
        cur.close()
        conn.close()

@router.get("/")
def get_favorites(current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, query, result, label, created_at
            FROM favorites
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (current_user["id"],))
        rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "query": row[1],
                "result": row[2],
                "label": row[3],
                "created_at": row[4]
            }
            for row in rows
        ]
    finally:
        cur.close()
        conn.close()

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM favorites
            WHERE id = %s AND user_id = %s
            RETURNING id
        """, (favorite_id, current_user["id"]))
        deleted = cur.fetchone()
        conn.commit()
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )
        return {"message": "Removed from favorites"}
    finally:
        cur.close()
        conn.close()