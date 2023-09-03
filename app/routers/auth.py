from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

# login endpoint
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm returns  in format {"username" : "abcde",  "password" : "password123"}

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user: # Email not found
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password): # password incorrect
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #create a token
    #return a token
    access_token = oauth2.create_access_token(data={"user_id" : user.id}) #, "user_email" : user.email

    return {'access_token' : access_token, 'token_type' : 'bearer'}
    