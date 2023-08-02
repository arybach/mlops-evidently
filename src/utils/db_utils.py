from typing import Callable, Union
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker

def open_sqa_session(arg: Union[str, sqlalchemy.engine.Engine]) -> sqlalchemy.orm.Session:
    if isinstance(arg, str):
        # If the argument is a string, treat it as the database URI
        engine = sqlalchemy.create_engine(arg)
    else:
        # If the argument is already an SQLAlchemy Engine, use it directly
        engine = arg

    Session: Callable = sessionmaker(bind=engine)
    session: sqlalchemy.orm.Session = Session()
    return session
