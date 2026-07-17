from sqlalchemy import Column, Integer, String, ForeignKey, Float
from db.base import Base

class Cutoff(Base):
    __tablename__ = "cutoffs"
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    category = Column(String)
    round = Column(Integer)
    year = Column(Integer)
    opening_rank = Column(Integer)
    closing_rank = Column(Integer)
    percentile = Column(Float)