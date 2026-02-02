import uuid
import enum
from sqlalchemy import String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin


class RequestStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class FriendRequest(Base, TimestampMixin):
    __tablename__ = "friend_requests"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    sender_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    receiver_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus),
        default=RequestStatus.PENDING
    )

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_friend_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_friend_requests")

    __table_args__ = (
        UniqueConstraint("sender_id", "receiver_id", name="unique_friend_request"),
    )


class Friendship(Base):
    __tablename__ = "friendships"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    friend_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[str] = mapped_column(String(36))

    __table_args__ = (
        UniqueConstraint("user_id", "friend_id", name="unique_friendship"),
    )
