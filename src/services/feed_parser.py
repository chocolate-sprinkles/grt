from .grt_client import fetch_rt_feed
from ..db.crud import upsert
from ..db.models import Metadata, TripUpdate, Vehicle, StopTimeUpdate
from sqlmodel import Session
from ..config import settings
from datetime import datetime

def process_trip_updates(session: Session) -> None:
    
    feed = fetch_rt_feed(settings.BASE_URL + settings.TRIP_UPDATES_ENDPOINT)

    upsert(
        session=session,
        record=Metadata(
            endpoint=settings.TRIP_UPDATES_ENDPOINT,
            gtfs_realtime_version=feed.header.gtfs_realtime_version,
            incrementality=feed.header.incrementality,
            server_timestamp=feed.header.timestamp
        )
    )

    for entity in feed.entity:

        vehicle_id = entity.trip_update.vehicle.id
        if vehicle_id not in (None, ''):
            upsert(
                session=session,
                record=Vehicle(id=int(vehicle_id))
            )

        upsert(
            session=session,
            record=TripUpdate(
                id=entity.trip_update.trip.trip_id,
                start_time=entity.trip_update.trip.start_time,
                start_date=datetime.strptime(entity.trip_update.trip.start_date, '%Y%m%d').date(),
                delay=entity.trip_update.delay,
                route_id=entity.trip_update.trip.route_id,
                reading_timestamp=entity.trip_update.timestamp,
                server_timestamp=feed.header.timestamp
            )
        )

        for stop_time_update in entity.trip_update.stop_time_update:

            upsert(
                session=session,
                record=StopTimeUpdate(
                    id=stop_time_update.stop_id,
                    trip_id=entity.trip_update.trip.trip_id,
                    stop_sequence=stop_time_update.stop_sequence,
                    arrival_time=stop_time_update.arrival.time,
                    arrival_delay=stop_time_update.arrival.delay,
                    departure_time=stop_time_update.departure.time,
                    departure_delay=stop_time_update.departure.delay,
                    schedule_relationship=stop_time_update.schedule_relationship,
                    reading_timestamp=feed.header.timestamp
                )
            )
            
    session.commit()