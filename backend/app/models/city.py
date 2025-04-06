from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship  
from app.config.database import Base

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, index=True)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)

    # Relationship: A city belongs to one country
    country = relationship("Country", back_populates="cities")
    hotels = relationship("Hotel", back_populates="city", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name}, country_id={self.country_id})>"
