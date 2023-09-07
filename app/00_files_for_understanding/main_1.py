from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

@app.get("/")
def greeting():
    return ["message", "Hello World"]

@app.get("/get_posts")
def get_post():
    return {"Message" : "Yous have recieved the post"}

# @app.post("/create_post")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"Message" : f"Title -> {payload['title']}   Content -> {payload['content']}"}


@app.post("/create_post")
def create_post(new_post: Post):
    print("Title is: ", new_post.title)
    print("Content is: ", new_post.content)
    print("Want to publish: ", new_post.publish)
    print("Rating given: ", new_post.rating)

    return {"data" : "new post"}