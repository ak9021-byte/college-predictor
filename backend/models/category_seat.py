from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base

class CategorySeat(Base):
    __tablename__ = "category_seats"
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    choice_code = Column(String, nullable=True)
    category = Column(String, nullable=False)
    general_seats = Column(Integer, default=0)
    ladies_seats = Column(Integer, default=0)
    total_seats = Column(Integer, default=0)
    round = Column(Integer, default=1)
    year = Column(Integer, default=2025)
    pwd_seats = Column(Integer, default=0)
    def_seats = Column(Integer, default=0)
    ews_seats = Column(Integer, default=0)
    tfws_seats = Column(Integer, default=0)