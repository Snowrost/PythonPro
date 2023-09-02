import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from core.db.mixins import TimestampMixin
from core.db import Base


class Meeting(Base, TimestampMixin):
    __tablename__ = 'meetings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_name = Column(String(55))
    date_of_activity = Column(DateTime(timezone=True))
