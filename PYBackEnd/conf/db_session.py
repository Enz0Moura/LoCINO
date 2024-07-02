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

def create_engine() -> Engine:
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_directory = os.path.join(project_root, 'db')

    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    """
    Function that sets the db connection.
    :return: Engine
    """
    global __engine

    if __engine:
        return __engine

    file_db = 'db/locino.sqlite'
    folder = Path(file_db).parent
    folder.mkdir(parents=True, exist_ok=True)
    conn_str = f'sqlite:///{file_db}'
    __engine = sa.create_engine(url=conn_str, echo=False, connect_args={'check_same_thread': False})
    return __engine
def create_session() -> Session:
    """
        Function that creates a db session.
        :return: Session
        """
    global __engine

    if not __engine:
        __engine = create_engine()

    __session = sessionmaker(bind=__engine, expire_on_commit=False, class_=Session)

    session: Session = __session()

    return session


def create_tables() -> None:
    if not __engine:
        create_engine()
    import models.__all_models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
