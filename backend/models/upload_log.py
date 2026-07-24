from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.base import Base

class UploadLog(Base):
    __tablename__ = "upload_logs"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="uploaded")
    row_count = Column(Integer, nullable=True)