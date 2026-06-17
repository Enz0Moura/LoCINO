import uuid

from models.model_base import ModelBase
import sqlalchemy as sa

class User(ModelBase):
    __tablename__: str = 'users'

    id: uuid = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    name: str = sa.Column(sa.String, nullable=False)
