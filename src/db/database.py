from sqlmodel import SQLModel, create_engine
from ..config import settings

DATABASE_URL = f"sqlite:///{settings.DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from . import models
    SQLModel.metadata.create_all(engine)