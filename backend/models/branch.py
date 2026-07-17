from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"))