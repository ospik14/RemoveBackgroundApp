from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    email: str = Field(min_length=5, max_length=100)
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=64)
    role: str = Field(max_length=20)

class ImageRequest(BaseModel):
    original_filename: str = Field(max_length=100) 
    processed_filename: str = Field(max_length=100) 
    owner_id: int
    created_at: str 

class CurrentUser:
    def __init__(self, username, user_id, role):
        self.username = username
        self.user_id = user_id
        self.role = role