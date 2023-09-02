from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID

import uuid
from sqlalchemy.orm import relationship
from core.db.mixins import TimestampMixin
from core.db import Base


class Feedback(Base,TimestampMixin):
    __tablename__ = 'feedback'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    meeting_id = Column(UUID(as_uuid=True), ForeignKey('meetings.id'))
    comment = Column(Text)

    meeting = relationship("Meeting")
    user = relationship("User")