from sqlalchemy import Column, Integer, String, Float
from db.base import Base

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    university = Column(String)

    status = Column(String, nullable=True)
    established = Column(String, nullable=True)
    website = Column(String, nullable=True)
    place = Column(String, nullable=True)
    naac_rating = Column(String, nullable=True)
    fees = Column(String, nullable=True)
    hostel_available = Column(String, nullable=True)
    students_placed_last_year = Column(Integer, nullable=True)
    highest_package = Column(String, nullable=True)
    average_package = Column(String, nullable=True)
    companies_visited = Column(Integer, nullable=True)