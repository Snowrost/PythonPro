from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import DECIMAL
from core.db.mixins import TimestampMixin
from core.db import Base


class Check(Base, TimestampMixin):
    __tablename__ = 'checks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    participant_id = Column(UUID(as_uuid=True), ForeignKey('participants.id'))
    custom_item_id = Column(UUID(as_uuid=True), ForeignKey('custom_items.id'))
    splited_bill = Column(DECIMAL(10, 3))

    participant = relationship("Participant")
    custom_item = relationship("CustomItem")

    def calculate_splited_bill(self):
        custom_item_price = self.custom_item.price
        participants_count = (
            self.participant.meeting.participants.filter_by(custom_item_id=self.custom_item_id).count()
        )
        self.splited_bill = custom_item_price / participants_count
