import uuid

from models.model_base import ModelBase
import sqlalchemy as sa
from datetime import datetime


class LocationHistory(ModelBase):
    __tablename__: str = 'locations_history'

    id: uuid = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    bracelet_id: uuid = sa.Column(sa.Uuid, sa.ForeignKey('bracelets.id'), nullable=False)
    location_time: datetime = sa.Column(sa.DateTime, nullable=False)
    register_time: datetime = sa.Column(sa.DateTime, nullable=False)
    battery: int = sa.Column(sa.Integer, nullable=False)
    latitude: float = sa.Column(sa.Float, nullable=False)
    longitude: float = sa.Column(sa.Float, nullable=False)