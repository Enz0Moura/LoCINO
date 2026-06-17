import uuid

from models.model_base import ModelBase
import sqlalchemy as sa


class Alert(ModelBase):
    __tablename__: str = 'alerts'

    id: uuid = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    location_history_id: uuid = sa.Column(sa.Uuid, sa.ForeignKey('locations_history.id'), nullable=False)
    alert_type: int = sa.Column(sa.Integer, nullable=False)
