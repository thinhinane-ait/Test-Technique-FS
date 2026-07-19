from sqlalchemy import String, DateTime, Enum,ForeignKey, Text,Enum,func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from datetime import datetime
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.antenna import Antenna

class InterventionPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Intervention(Base):
    __tablename__="intervention"

    id: Mapped[int] = mapped_column(
        primary_key=True,

    )
    
    antenna_id: Mapped[int] = mapped_column(
        ForeignKey("antenna.id", ondelete="CASCADE"),
        nullable=False,
        index=True, 
        )
    
    description: Mapped[str] = mapped_column(
       Text,
       nullable=False,
    )

    technician_identity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    priority: Mapped[InterventionPriority] = mapped_column(
        Enum(InterventionPriority, name="intervention_priority"),
        nullable=False,
        default=InterventionPriority.MEDIUM,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    ended_at: Mapped[datetime |None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    antenna: Mapped[Antenna] = relationship(
        back_populates='intervention'
    )


    




     
