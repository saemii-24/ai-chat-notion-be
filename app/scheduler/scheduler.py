from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler.jobs import pick_top_post

scheduler = AsyncIOScheduler()


def register_jobs():
    scheduler.add_job(
        pick_top_post,
        trigger="interval",
        minutes=1,
        id="pick_top_post_job",
        replace_existing=True,
    )
