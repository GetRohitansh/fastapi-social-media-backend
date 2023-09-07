# Integrated with database and using ORM
# Using Routers to make code maintainable

from fastapi import FastAPI
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# from .database import engine
# from . import models


# alembic takes care of table generation, hence we remove sqlalchemy engine
# models.Base.metadata.create_all(bind=engine) # creates a table in our database

app = FastAPI()


# CORS 

origins = ['https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def message():
    return {"message" : "Hello World"}