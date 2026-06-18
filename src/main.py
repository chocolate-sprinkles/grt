from .services.feed_parser import process_trip_updates
from .services.feed_parser import process_trip_updates
from sqlmodel import Session
from pathlib import Path
from .db.database import engine, init_db
from .config import Settings
from .services.grt_client import fetch_static_feed
from .services.text_parser import ingest_text_files
from .config import Settings
import time
import shutil

def main():

    settings = Settings()

    if Path.exists(settings.DB_PATH):
        settings.DB_PATH.unlink()
        print('Old DB deleted.')

    init_db()

    with Session(engine) as session:

        process_trip_updates(session=session)
        time.sleep(3)
        fetch_static_feed(settings.BASE_URL + settings.STATIC_FEED_ENDPOINT)
        ingest_text_files(session=session)

    if Path.exists(settings.ZIP_PATH):
        shutil.rmtree(settings.ZIP_PATH)
        print('Deleting static contents')

if __name__ == "__main__":
    main()
    