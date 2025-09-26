from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str
    code: str 
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# New Schema for the request body of the save playlist endpoint
class PlaylistPayload(BaseModel):
    """
    Defines the structure for the incoming playlist data in the request body.
    It expects a JSON object with a key "songs" which is a list of strings.
    e.g., {"songs": ["path/to/song1.mp3", "path/to/song2.mp3"]}
    """
    songs: List[str]

# New Schema for returning a list of playlist names
class PlaylistsListResponse(BaseModel):
    """
    Defines the structure for the response containing a list of playlist names.
    e.g., {"names": ["My Favorites", "Podcasts"]}
    """
    names: List[str]

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
