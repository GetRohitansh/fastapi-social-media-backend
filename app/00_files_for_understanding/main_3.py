# Integrated with database and using SQL queries
import time
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange # to give random unique id to objects inside 'my_post' database
import psycopg2 # for database
from psycopg2.extras import RealDictCursor # to get column name along with data (like dictionary)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True: # To reconnect database after connection is failed
    try:
        # connecting to database
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres', password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor() # used to execute SQL queries
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)



@app.get("/get_posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"data" : posts}


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new data" : new_post}


@app.get("/get_post/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id), ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    return {"post_detail": post}


@app.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/update_post/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """, 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"updated_data" : updated_post}