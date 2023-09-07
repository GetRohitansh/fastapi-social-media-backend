# Integrated with database and using ORM
# Post and User in same file
from typing import List
import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2 # for database
from psycopg2.extras import RealDictCursor # to get column name along with data (like dictionary)
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .utils import hash


models.Base.metadata.create_all(bind=engine) # creates a table in our database

app = FastAPI()

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


@app.get("/get_posts", response_model=List[schemas.Post]) # Gives list of schema.Post model
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict()) # unpack as dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post that we commited and store inside new_post
    return new_post


@app.get("/get_post/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    return post


@app.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/update_post/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit() 
    return post.first()


##########################################################################################################
#       USER Methods        #
@app.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hashing the password
    user.password = hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/get_user/{id}", response_model=schemas.UserOut)
def get_post(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} was not found")
    
    return user