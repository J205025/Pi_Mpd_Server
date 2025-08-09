from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str


    class Config:
        orm_mode = True

    
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserPlaylistBase(BaseModel):
    playlist_name: str
    playlist_data: str # Will store JSON string of file paths

class UserPlaylistCreate(UserPlaylistBase):
    pass

class UserPlaylistResponse(UserPlaylistBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True