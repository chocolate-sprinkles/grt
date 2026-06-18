from .grt_client import fetch_static_feed
from ..db.crud import upsert
from ..db.models import Agency, Calendar, CalendarDates, Routes, Stops, StopTimes, Trips
from sqlmodel import Session
from ..config import Settings
import csv
from datetime import datetime

def _ingest_agency(session: Session, reader: csv.DictReader) -> None:
    
    for row in reader:
    
        upsert(
            session=session, 
            record=Agency(
            id=1,
            name=row['agency_name'],
            url=row['agency_url'],
            phone=row['agency_phone'],
            fare_url=row['agency_fare_url'],
            )
        )

def _ingest_calendar(session: Session, reader: csv.DictReader) -> None:
    
    for row in reader:

        upsert(
            session=session, 
            record=Calendar(
            service_id=row['service_id'],
            monday=row['monday'],
            tuesday=row['tuesday'],
            wednesday=row['wednesday'],
            thursday=row['thursday'],
            friday=row['friday'],
            saturday=row['saturday'],
            sunday=row['sunday'],
            start_date=datetime.strptime(row['start_date'], '%Y%m%d').date(),
            end_date=datetime.strptime(row['end_date'], '%Y%m%d').date(),
            )
        )

def _ingest_calendar_dates(session: Session, reader: csv.DictReader) -> None:

    for row in reader:

        upsert(
            session=session,
            record=CalendarDates(
                service_id=row['service_id'],
                cal_date=datetime.strptime(row['date'], '%Y%m%d').date(),
                exception_type=row['exception_type']
            )
        )

def _ingest_routes(session: Session, reader: csv.DictReader) -> None:

    for row in reader:

        upsert(
            session=session,
            record=Routes(
                id=row['route_id'],
                short_name=row['route_short_name'],
                long_name=row['route_long_name'],
                desc=row['route_desc'],
                type=row['route_type'],
                url=row['route_url'],
                color=row['route_color'],
                text_color=row['route_text_color']
            )
        )

def _ingest_stops(session: Session, reader: csv.DictReader) -> None:

    for row in reader:

        upsert(
            session=session,
            record=Stops(
                id=row['stop_id'],
                name=row['stop_name'],
                lat=row['stop_lat'],
                long=row['stop_lon']
            )
        )

def _ingest_stop_times(session: Session, reader: csv.DictReader) -> None:
    
    for row in reader:

        upsert(
            session=session,
            record=StopTimes(
                stop_id=row['stop_id'],
                trip_id=row['trip_id'],
                stop_sequence=row['stop_sequence'],
                arrival_time=row['arrival_time'],
                departure_time=row['departure_time']
            )
        )

def _ingest_trips(session: Session, reader: csv.DictReader) -> None:
    
    for row in reader:

        upsert(
            session=session,
            record=Trips(
                id=row['trip_id'],
                route_id=row['route_id'],
                service_id=row['service_id'],
                headsign=row['trip_headsign'],
                direction_id=row['direction_id'],
            )
        )

INGEST_MAPPING = {
    'agency.txt': _ingest_agency,
    'calendar.txt': _ingest_calendar,
    'calendar_dates.txt': _ingest_calendar_dates,
    'routes.txt': _ingest_routes,
    'stops.txt': _ingest_stops,
    'stop_times.txt': _ingest_stop_times,
    'trips.txt': _ingest_trips
}

def ingest_text_files(session: Session) -> None:
    settings = Settings()

    for file in fetch_static_feed(settings.BASE_URL + settings.STATIC_FEED_ENDPOINT):

        with open(file, mode='r', encoding='utf-8') as f:
            if file.name in INGEST_MAPPING:
                reader = csv.DictReader(f)
                INGEST_MAPPING[file.name](session, reader)

        session.commit()
