from .services.feed_parser import process_trip_updates
from .services.feed_parser import process_trip_updates
from sqlmodel import Session
from pathlib import Path
from .db.database import engine, init_db
from .config import settings
from .services.grt_client import fetch_static_feed
from .services.text_parser import ingest_text_files
import time
import shutil

def main():

    if Path.exists(settings.DB_PATH):
        settings.DB_PATH.unlink()
        print('Old DB deleted.')

    init_db()

    with Session(engine) as session:

        process_trip_updates(session=session)
        time.sleep(3)
        ingest_text_files(session=session)

    if Path.exists(settings.ZIP_PATH):
        shutil.rmtree(settings.ZIP_PATH)
        print('Deleting static contents')

if __name__ == "__main__":
    main()
    