from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    JSON,
    String,
    Table,
    Column,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", BigInteger, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
)


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        back_populates="building", lazy="selectin"
    )


class ActivityModel(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), nullable=True
    )
    level: Mapped[int] = mapped_column(default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="check_activity_level"),
    )

    parent: Mapped["ActivityModel | None"] = relationship(
        back_populates="children", remote_side=[id], lazy="joined"
    )
    children: Mapped[list["ActivityModel"]] = relationship(
        back_populates="parent", lazy="selectin"
    )
    organizations: Mapped[list["OrganizationModel"]] = relationship(
        secondary=organization_activity, back_populates="activities", lazy="selectin"
    )


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phones: Mapped[list[str]] = mapped_column(JSON, default=list)
    building_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    building: Mapped["BuildingModel"] = relationship(
        back_populates="organizations", lazy="joined"
    )
    activities: Mapped[list["ActivityModel"]] = relationship(
        secondary=organization_activity, back_populates="organizations", lazy="selectin"
    )
