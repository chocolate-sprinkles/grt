from sqlmodel import Session, SQLModel

def upsert(session: Session, record: SQLModel) -> None:
    session.merge(record)
