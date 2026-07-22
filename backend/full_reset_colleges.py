from db.session import SessionLocal
from models.category_seat import CategorySeat
from models.branch import Branch
from models.college import College

db = SessionLocal()
c1 = db.query(CategorySeat).delete()
c2 = db.query(Branch).delete()
c3 = db.query(College).delete()
db.commit()
db.close()
print(f"Deleted {c1} category_seats, {c2} branches, {c3} colleges")