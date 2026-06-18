from requests.adapters import HTTPAdapter
import ssl
import requests
from google.transit import gtfs_realtime_pb2
import time
from typing import List
import zipfile
import io 
from ..config import Settings

class CustomSSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)
    
def fetch_rt_feed(endpoint: str) -> gtfs_realtime_pb2.FeedMessage: 
        
        session = requests.Session()  
        session.mount("https://", CustomSSLAdapter())

        response = session.get(endpoint)
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()

        retries = 3
        successful = False

        while retries > 0:

            try:
                feed.ParseFromString(response.content)
                retries = 0
                successful = True
                return feed
            except Exception as e:
                print(f'Exception {e} has occurred. Retrying in 5 seconds. {retries} attempts left.')
                time.sleep(5)
                retries -= 1

        if not successful:
            raise Exception('Something went wrong with the feed.')
    
def fetch_static_feed(endpoint: str) -> List[str]:
        
        settings = Settings()

        session = requests.Session()  
        session.mount("https://", CustomSSLAdapter())

        response = session.get(endpoint)
        response.raise_for_status()

        file_paths = []

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall(settings.ZIP_PATH)
            
            for name in zf.namelist():
                file_paths.append(settings.ZIP_PATH / name)
                    
            return file_paths

        
