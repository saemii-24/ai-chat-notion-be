from sqlalchemy import select, desc
from app.db.db import SessionLocal
from app.post.models import Post, TopPost


async def pick_top_post():
    async with SessionLocal() as db:
        result = await db.execute(select(Post).order_by(desc(Post.like_count)).limit(1))
        top_post = result.scalar_one_or_none()

        if top_post is None:
            print("No posts found")
            return

        record = TopPost(post_id=top_post.id)
        db.add(record)
        await db.commit()

        print(f"Top post saved: {top_post.id}")
