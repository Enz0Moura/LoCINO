import uuid

from models.model_base import ModelBase
import sqlalchemy as sa

class Bracelet(ModelBase):
    __tablename__: str = 'bracelets'

    id: uuid = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    user_id: uuid = sa.Column(sa.Uuid, sa.ForeignKey('users.id'), nullable=False)