import os
from typing import Callable, Union
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker

def open_sqa_session(arg: Union[str, sqlalchemy.engine.Engine]) -> sqlalchemy.orm.Session:
    if isinstance(arg, str):
        # If the argument is a string, treat it as the database URI
        # engine_args = {}
        # ssl_cert_path = os.getenv("SSL_CERT_PATH")
        # ssl_key_path = os.getenv("SSL_KEY_PATH")
        # if ssl_cert_path is not None and ssl_key_path is not None:
        #     engine_args["connect_args"] = {
        #         "sslmode": "require",
        #         "sslcert": ssl_cert_path,
        #         "sslkey": ssl_key_path,
        #     }
        engine = sqlalchemy.create_engine(arg)
    else:
        # If the argument is already an SQLAlchemy Engine, use it directly
        engine = arg

    Session: Callable = sessionmaker(bind=engine)
    session: sqlalchemy.orm.Session = Session()
    return session
