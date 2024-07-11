import uuid

from models.model_base import ModelBase
from datetime import datetime
import sqlalchemy as sa
class Message(ModelBase):
    __tablename__: str = 'messages'

    id: uuid = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    success: bool = sa.Column(sa.Boolean, nullable=False)
    group_id: int = sa.Column(sa.Integer, nullable=True)
    message: str = sa.Column(sa.VARCHAR(450), nullable=True)
    battery: int = sa.Column(sa.Integer, nullable=True)
    channel: int = sa.Column(sa.Integer, nullable=True)
    group_flag: bool = sa.Column(sa.Boolean, nullable=True)
    hop_count: int = sa.Column(sa.Integer, nullable=True)
    help_flag: int = sa.Column(sa.Integer, nullable=True)
    latitude: float = sa.Column(sa.Float, nullable=True)
    longitude: float = sa.Column(sa.Float, nullable=True)
    location_time: datetime = sa.Column(sa.DateTime, nullable=False)
    max_records: int = sa.Column(sa.Integer, nullable=True)
    message_type: bool = sa.Column(sa.Boolean, nullable=True)
    record_time: datetime = sa.Column(sa.DateTime, nullable=True)
    received_at: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
