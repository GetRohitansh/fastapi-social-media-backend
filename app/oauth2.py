# Functions related to authentication

''' 
Whenever we need to protect endpoint(route) which means user needs to be logged in to use it,
we pass get_current_user as its dependency.
'''

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import Settings

#secret_key (any random long string)
#algorithm
#expriation time (for how much time should user be logged in)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  # login endpoint

SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str, credential_exceptions):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")
        # email: str = payload.get("user_email")

        if id is None:
            raise credential_exceptions
        # if email is None:
        #     raise credential_exceptions
        
        token_data = schemas.TokenData(id=id) # , email=email

    except JWTError:
        raise credential_exceptions
    
    return token_data # returns user_id

    

# we can pass this as dependency to other routes 
# get token and verify it
# extract id and return id
# fetch user from database
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
 
     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                           detail="Could not Validate Credentials", 
                                           headers={'WWW-AUTHENTICATE' : 'Bearer'})
     
     token = verify_access_token(token, credentials_exception)
     user = db.query(models.User).filter(models.User.id == token.id).first()
     
     return user
     
