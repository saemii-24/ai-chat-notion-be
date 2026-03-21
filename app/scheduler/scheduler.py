from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.jobs import pick_top_post

scheduler = BackgroundScheduler()


def register_jobs():
    scheduler.add_job(
        pick_top_post,
        trigger="interval",
        seconds=10,
        id="pick_top_post_job",
        replace_existing=True,
    )
