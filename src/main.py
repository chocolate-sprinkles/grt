from .services.feed_parser import process_trip_updates
from sqlmodel import Session
from pathlib import Path
from .db.database import engine, init_db
from .config import settings
from .services.text_parser import ingest_text_files
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def realtime_job():
    with Session(engine) as session:
        print(f'Processing feed at {str(datetime.now())}')
        process_trip_updates(session=session)

def main():
    if Path.exists(settings.DB_PATH):
        settings.DB_PATH.unlink()
        print("Old DB deleted.")

    init_db()

    with Session(engine) as session:
        ingest_text_files(session=session)

    scheduler = BlockingScheduler()
    scheduler.add_job(
        realtime_job,
        trigger='interval',
        seconds=settings.REAL_TIME_FEED_REFRESH_SECONDS,
        id='realtime_feed',
        max_instances=1,
        misfire_grace_time=10
    )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
    finally:
        if Path.exists(settings.ZIP_PATH):
            shutil.rmtree(settings.ZIP_PATH)
            print("Deleting static contents.")

if __name__ == "__main__":
    main()