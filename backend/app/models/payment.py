from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Payment ID
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)  # Reference to Booking
    payment_date = Column(Date, nullable=False)  # Date when payment was made
    payment_method = Column(String(50), nullable=False)  # Payment method (e.g., "Credit Card", "UPI")
    amount = Column(Float, nullable=False)  # Total payment amount

    # Relationship with Booking (One-to-One)
    booking = relationship("Booking", back_populates="payment", uselist=False)  # One payment per booking

    def __repr__(self):
        return f"<Payment(id={self.id}, booking_id={self.booking_id}, amount={self.amount}, payment_date={self.payment_date}, payment_method={self.payment_method})>"
