from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

scheduler = BlockingScheduler()


def test_job():
    print(f"[스케쥴러] 실행됨: {datetime.now()}")


scheduler.add_job(test_job, "interval", minutes=1)

if __name__ == "__main__":
    print("[스케쥴러] started")
    scheduler.start()
