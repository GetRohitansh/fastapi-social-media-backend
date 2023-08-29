from typing import List, Optional
from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(tags=['Posts']) # tags helps in grouping api in swagger api documentation

# @router.get("/posts", response_model=List[schemas.Post]) # Gives list of schema.Post model
@router.get("/posts" , response_model=List[schemas.Post_Vote_Out])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
               limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    '''Path Parameters'''
    # default limit is 10
    # skip: how many number of posts to skip
    # default skip is 0
    # search with the name of title
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return posts

    # adding join query
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    # adding filters
    posts = posts.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # dependencies are session and authentication
    # dependency: only authenticated / logged in user can create posts
    print(current_user)    
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # owner_id + unpack post as dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post that we commited and store inside new_post
    return new_post


# @router.get("/posts/{id}", response_model=schemas.Post)
@router.get("/posts/{id}", response_model=schemas.Post_Vote_Out)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    '''
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    return post
    '''

    # adding join query
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    # adding filters
    post = post.filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id) # post to delete
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit() 
    return post.first()