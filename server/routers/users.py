from fastapi import APIRouter
from pydantic import BaseModel

from database.sql import create_connection
from encryption import hash_password


class User(BaseModel):
    uid: str
    username: str
    password: str


router = APIRouter()


@router.post("/api/users/", response_model=User)
async def create(user: User):
    connection = create_connection()
    cur = connection.cursor()
    db_user = User(
        uid="dsfdasfasefs",
        username=user.username,
        password=hash_password(user.password),
    )
    cur.execute(
        """INSERT INTO User (userID, username, password) VALUES (?,?,?)""",
        (db_user.uid, db_user.username, db_user.password),
    )
    connection.commit()
    connection.close()
    return db_user


@router.get("/api/users/{username}")
async def read(username: str):
    connection = create_connection(db)
    cur = connection.cursor()
    cur.execute("""SELECT * FROM Customer WHERE username = ?""", (username,))
    user = cur.fetchone()
    connection.close()
    return user
