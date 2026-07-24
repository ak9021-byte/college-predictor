from db.session import SessionLocal
from models.cutoff import Cutoff

db = SessionLocal()
deleted = db.query(Cutoff).delete()
db.commit()
db.close()
print(f"Deleted {deleted} cutoff rows")