from sqlalchemy import Column, Integer, String
from db.base import Base

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    university = Column(String)