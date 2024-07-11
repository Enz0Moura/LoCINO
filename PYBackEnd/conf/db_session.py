import os
import sys
from pathlib import Path
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.future.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from models.model_base import ModelBase
__engine: Optional[Engine] = None

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

username = 'totem'
password = 'teste123'
host = '192.168.1.17'
database = 'colaborative_local'
DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database}"



def create_engine(use_my_sql: bool=False) -> Engine:
    """
        Function that sets the db connection.
        :return: Engine
    """
    global __engine
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_directory = os.path.join(project_root, 'db')

    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    if __engine:
        return __engine
    if not use_my_sql:
        file_db = 'db/locino.sqlite'
        folder = Path(file_db).parent
        folder.mkdir(parents=True, exist_ok=True)
        conn_str = f'sqlite:///{file_db}'
        __engine = sa.create_engine(url=conn_str, echo=False, connect_args={'check_same_thread': False})
    else:
        __engine = sa.create_engine(DATABASE_URL, echo=True)
    return __engine
def create_session(use_my_sql: bool=False) -> Session:
    """
        Function that creates a db session.
        :return: Session
        """
    global __engine

    if not __engine:
        __engine = create_engine(use_my_sql)

    __session = sessionmaker(bind=__engine, expire_on_commit=False, class_=Session)

    session: Session = __session()

    return session


def create_tables(use_my_sql: bool=False) -> None:
    global __engine

    if not __engine:
        create_engine(use_my_sql)
    import models.__all_models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
