import uuid

from models.model_base import ModelBase
import sqlalchemy as sa

class Contact(ModelBase):
    __tablename__: str = 'contacts'

    id: uuid = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    user_id: uuid = sa.Column(sa.Uuid, sa.ForeignKey('users.id'), nullable=False)
    name: str = sa.Column(sa.String, nullable=False)
    telephone: str = sa.Column(sa.String, nullable=False)
    email: str = sa.Column(sa.String, nullable=True)