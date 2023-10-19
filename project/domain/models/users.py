import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(55))
    lastname = Column(String(120))
    password = Column(String(255))
    email = Column(String(150))