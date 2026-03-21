import time

from app.scheduler.scheduler import scheduler, register_jobs


def main():
    register_jobs()
    scheduler.start()
    print("Scheduler started")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped")


if __name__ == "__main__":
    main()
