from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.db import SessionLocal
from app.post.models import Post, TopPost


def pick_top_post():
    db: Session = SessionLocal()
    try:
        top_post = db.query(Post).order_by(Post.like_count.desc()).first()

        if top_post is None:
            print("No posts found")
            return

        record = TopPost(post_id=top_post.id)
        db.add(record)
        db.commit()

        print(f"Top post saved: {top_post.id}")
    finally:
        db.close()
