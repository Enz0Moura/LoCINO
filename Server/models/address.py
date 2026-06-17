import uuid

from models.model_base import ModelBase
import sqlalchemy as sa

class Address(ModelBase):
    __tablename__: str = 'addresses'

    id: uuid = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    user_id: uuid = sa.Column(sa.Uuid, sa.ForeignKey('users.id'), nullable=False)
    street: str = sa.Column(sa.String, nullable=False)
    neighborhood: str = sa.Column(sa.String, nullable=False)
    city: str = sa.Column(sa.String, nullable=False)
    state: str = sa.Column(sa.String, nullable=False)