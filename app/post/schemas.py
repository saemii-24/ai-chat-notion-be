from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostList(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    like_count: int

    class Config:
        orm_mode = True # 이를 통해 SQLAlchemy 모델을 Pydantic 모델로 변환할 때 ORM 객체를 사용할 수 있다.