from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from skylock.config import DATABASE_URL


def get_db_session():
    engine = create_engine(DATABASE_URL)
    factory = sessionmaker(bind=engine)
    with factory() as session:
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
