from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    content: str


class PostList(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    like_count: int

    model_config = ConfigDict(from_attributes=True)


class PostDetail(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    like_count: int

    model_config = ConfigDict(from_attributes=True)
