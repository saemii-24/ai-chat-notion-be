from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class GetPost(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    like_count: int

    class Config:
        orm_mode = True  