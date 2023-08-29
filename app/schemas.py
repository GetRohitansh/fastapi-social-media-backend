from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Response (in postman all details of owner of post that we want to return is defined here)
class Owner_Post_Out(BaseModel):
    id: int
    email: EmailStr
    class Config: #Converts sqlalchemy model to pydantic model
        from_attributes = True

# Response (in postman all details of post that we want to return is defined here)
class Post(PostBase):
    id: int
    created_at: datetime 
    owner: Owner_Post_Out
    class Config: #Converts sqlalchemy model to pydantic model
        from_attributes = True


# Response with number of votes and other fields
class Post_Vote_Out(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


###################################################################################
#       USER        #
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: #Converts sqlalchemy model to pydantic model
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

##################################################################################
#       Token       #

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    # email: Optional[str] = None


####################################################################################
#       Votes       #
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)