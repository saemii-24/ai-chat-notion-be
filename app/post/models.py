from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    like_count = Column(Integer, default=0, nullable=False)

    author = relationship("User")
    top_post_records = relationship("TopPost", back_populates="post")


class TopPost(Base):
    __tablename__ = "top_posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    picked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="top_post_records")
