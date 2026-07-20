from sqlalchemy import Column, Integer, String
from db.base import Base

class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)