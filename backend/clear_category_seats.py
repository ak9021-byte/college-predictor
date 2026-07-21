from db.session import SessionLocal
from models.category_seat import CategorySeat

db = SessionLocal()
deleted = db.query(CategorySeat).delete()
db.commit()
db.close()
print(f"Deleted {deleted} category_seat rows")