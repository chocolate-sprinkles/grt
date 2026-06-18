from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):

    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DB_PATH: Path = PROJECT_ROOT / 'grt.db'
    ZIP_PATH: Path = PROJECT_ROOT / 'zip_contents'

    BASE_URL: str = 'https://webapps.regionofwaterloo.ca/api/grt-routes/api'

    TRIP_UPDATES_ENDPOINT: str = '/tripupdates/2'
    VEHICLE_POSITIONS_ENDPOINT: str = '/vehiclepositions2/2'
    SERVICE_ALERTS_ENDPOINT: str = '/servicealerts/2'
    STATIC_FEED_ENDPOINT: str = '/staticfeeds/2'

    DB_ECHO: bool = False 

    REAL_TIME_FEED_REFRESH_SECONDS: int = 30

settings = Settings()