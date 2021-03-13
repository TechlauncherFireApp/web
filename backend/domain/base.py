from contextlib import contextmanager

from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure Session
Session = sessionmaker()
engine = create_engine('mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(os.environ.get('MYSQL_USER'),
                                                                    os.environ.get('MYSQL_PASSWORD'),
                                                                    os.environ.get('MYSQL_HOST'),
                                                                    os.environ.get('MYSQL_PORT'),
                                                                    os.environ.get('MYSQL_DATABASE')))
Session.configure(bind=engine)

# Configure Declarative Base for ORM
Base = declarative_base()
Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
