import uuid
import enum
from sqlalchemy import String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin


class RoomType(enum.Enum):
    PRIVATE = "private"  # 一對一私聊
    GROUP = "group"      # 多人群組


class MemberRole(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class Room(Base, TimestampMixin):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    type: Mapped[RoomType] = mapped_column(Enum(RoomType), default=RoomType.PRIVATE)

    # Relationships
    members = relationship("RoomMember", back_populates="room", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="room", cascade="all, delete-orphan")


class RoomMember(Base):
    __tablename__ = "room_members"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    room_id: Mapped[str] = mapped_column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"))
    role: Mapped[MemberRole] = mapped_column(Enum(MemberRole), default=MemberRole.MEMBER)

    user = relationship("User", back_populates="room_memberships")
    room = relationship("Room", back_populates="members")

    __table_args__ = (
        UniqueConstraint("user_id", "room_id", name="unique_room_member"),
    )
