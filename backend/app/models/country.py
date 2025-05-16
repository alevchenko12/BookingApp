from sqlalchemy import Column, Integer, String
from app.config.database import Base
from sqlalchemy.orm import relationship

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(120), unique=True, nullable=False, index=True)

    # Relationship: A country can have multiple cities
    cities = relationship("City", back_populates="country", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Country(id={self.id}, name={self.name})>"
