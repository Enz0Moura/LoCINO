import uuid

from PYBackEnd.models.model_base import ModelBase
from datetime import datetime
import sqlalchemy as sa
class Message(ModelBase):
    __tablename__: str = 'messages'

    id: uuid = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    success: bool = sa.Column(sa.Boolean, nullable=False)
    message: str = sa.Column(sa.String, nullable=True)
    recieved_at: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    