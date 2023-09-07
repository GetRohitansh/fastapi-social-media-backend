# List used as database here

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
# to give random unique id to objects inside 'my_post' database
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


my_post = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
]

# function to find the requires post


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

# function to find the index of post


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.get("/")
def greeting():
    return {"message": "Hello World"}


@app.get("/get_posts")
def get_posts():
    return {"data": my_post}

# Whenever we create post status code should be 201
# @app.post("/create_post")


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    # large range mostly gives unique numbers
    post_dict['id'] = randrange(0, 1000000)
    my_post.append(post_dict)
    return {"data": post_dict}


@app.get("/get_post/latest")
def get_latest_post():  # it automatically converts to integer
    post = my_post[len(my_post)-1]
    return {"latest data": post}

# id can only be integer but here input is string
    # @app.get("/get_post/{id}")
    # def get_post(id):
    #     post = find_post(int(id))
    #     return {"data" : post}

# to provide validation to enter only integer is


@app.get("/get_post/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id {id} was not found"}
    return {"post_detail": post}


@app.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    my_post.pop(index)
    return {"message": "post deleted succesfully"} # Data does not return as we delete a content
    # return Response(status_code=status.HTTP_204_NO_CONTENT) # ideally we should return this as no data is returned


@app.put("/update_post/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data" : post_dict}