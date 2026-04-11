from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    background_image_key: str | None = None

    model_config = ConfigDict(from_attributes=True)


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
