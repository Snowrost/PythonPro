from sqlalchemy import Column, String, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.db.mixins import TimestampMixin
from core.db import Base


class CustomItem(Base,TimestampMixin):
    __tablename__ = 'custom_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_name = Column(String(255))
    price = Column(DECIMAL(10, 2))
