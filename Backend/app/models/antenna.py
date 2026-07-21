#app/models/antenna.py
from __future__ import annotations
from sqlalchemy import String, DateTime, Enum, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from datetime import datetime
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from app.models.intervention import Intervention


class AntennaStatus(str, enum.Enum):
    UP = "UP"
    DOWN = "DOWN"


class Antenna(Base):
    __tablename__="antenna"

    id: Mapped[int] = mapped_column(
        primary_key=True,

    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    status: Mapped[AntennaStatus] = mapped_column(
     Enum(AntennaStatus, name="antenna_status"),
     nullable=False,
     default=AntennaStatus.UP,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    interventions: Mapped[list["Intervention"]] = relationship(
        back_populates="antenna",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin"
    )



