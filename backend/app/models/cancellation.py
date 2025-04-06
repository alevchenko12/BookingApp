from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Cancellation(Base):
    __tablename__ = "cancellations"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), unique=True, nullable=False)
    cancellation_date = Column(Date, nullable=False)
    refund_amount = Column(Float, nullable=False, default=0.0)

    # Relationship back to Booking
    booking = relationship("Booking", back_populates="cancellation", uselist=False)

    def __repr__(self):
        return f"<Cancellation(id={self.id}, booking_id={self.booking_id}, date={self.cancellation_date}, refund={self.refund_amount})>"
