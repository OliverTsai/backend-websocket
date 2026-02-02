import uuid
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    content: Mapped[str] = mapped_column(Text)
    sender_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    room_id: Mapped[str] = mapped_column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    sender = relationship("User", back_populates="sent_messages")
    room = relationship("Room", back_populates="messages")

    __table_args__ = (
        Index("idx_messages_room_created", "room_id", "created_at"),
    )
