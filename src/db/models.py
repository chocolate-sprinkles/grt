from sqlmodel import SQLModel, Field, create_engine
from pydantic import field_validator
from typing import Optional
from datetime import datetime, date

# Static Feed
class Agency(SQLModel, table=True):
    id: int = Field(default = None, primary_key=True)
    name: str
    url: str
    timezone: str = Field(default='est')
    language: str = Field(default='en')
    phone: int
    fare_url: str

    @field_validator('phone', mode='before')
    @classmethod
    def parse_phone(cls, v):
        if isinstance(v, str):
            return int(v.replace("-", ""))
        return v

class Calendar(SQLModel, table=True):
    service_id: str = Field(default=None, primary_key=True, min_length=4, max_length=4)
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int
    sunday: int
    start_date: date = Field(primary_key=True)
    end_date: date = Field(primary_key=True)

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_start_date(cls, v):        
        pattern='%Y%m%d'
        if isinstance(v, str):
            return datetime.strptime(v, pattern).date()
        elif isinstance(v, int):
            return datetime.strptime(str(v), pattern).date()
        return v

class CalendarDates(SQLModel, table=True):
    __tablename__ = 'calendar_dates'
    service_id: str = Field(default=None, primary_key=True, min_length=4, max_length=4) 
    cal_date: date = Field(primary_key=True)
    exception_type: int

    @field_validator('cal_date', mode='before')
    @classmethod
    def parse_start_date(cls, v):        
        pattern='%Y%m%d'
        if isinstance(v, str):
            return datetime.strptime(v, pattern).date()
        elif isinstance(v, int):
            return datetime.strptime(str(v), pattern).date()
        return v

class Routes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    short_name: str
    long_name: Optional[str]
    desc: Optional[str]
    type: int
    url: str
    color: str
    text_color: str

class Stops(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    lat: str
    long: str

class Trips(SQLModel, table=True):
    id: int = Field(primary_key=True)
    route_id: int = Field(foreign_key='routes.id')
    service_id: int = Field(foreign_key='calendar.service_id')
    headsign: str
    direction_id: str

class StopTimes(SQLModel, table=True):
    __tablename__ = 'stop_times'
    stop_id: int = Field(primary_key=True, foreign_key='stops.id')
    trip_id: int = Field(primary_key=True, foreign_key='trips.id')
    stop_sequence: int = Field(primary_key=True)
    arrival_time: str
    departure_time: str


# Real-Time Feed
class Metadata(SQLModel, table=True):
    endpoint: str = Field(primary_key=True)
    gtfs_realtime_version: str
    incrementality: str
    server_timestamp: int = Field(primary_key=True)

    @field_validator('incrementality', mode='before')
    @classmethod
    def parse_incrementality(cls, v):
        incrementality_mapping = {
            0:'FULL_DATASET',
            1:'PARTIAL_DATASET'
        }
        if isinstance(v, int):
            return incrementality_mapping[v]
        elif isinstance(v, str):
            return incrementality_mapping[int(v)]
        else:
            print(type(v))
            return v

class Vehicle(SQLModel, table=True):
    id: int = Field(primary_key=True)
    last_day_active: date = Field(default_factory=lambda: datetime.now().date())

class TripUpdate(SQLModel, table=True):
    __tablename__ = 'trip_update'
    id: int = Field(primary_key=True)
    start_time: str
    start_date: date
    delay: Optional[int]
    route_id: int = Field(foreign_key='routes.id')
    reading_timestamp: int = Field(primary_key=True)
    server_timestamp: int = Field(primary_key=True)

    @field_validator('start_date', mode='before')
    @classmethod
    def parse_start_date(cls, v):        
        pattern='%Y%m%d'
        if isinstance(v, str):
            return datetime.strptime(v, pattern).date()
        elif isinstance(v, int):
            return datetime.strptime(str(v), pattern).date()
        return v

class StopTimeUpdate(SQLModel, table=True):
    __tablename__ = 'stop_time_update'
    id: int = Field(primary_key=True)
    trip_id: int = Field(foreign_key='trip_update.id')
    stop_sequence: int
    arrival_time: int
    arrival_delay: int
    departure_time: int
    departure_delay: int    
    schedule_relationship: int
    reading_timestamp: int = Field(primary_key=True)

