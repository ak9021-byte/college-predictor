from db.session import SessionLocal
from models.branch import Branch
from models.college import College

db = SessionLocal()
deleted_branches = db.query(Branch).delete()
deleted_colleges = db.query(College).delete()
db.commit()
db.close()

print(f"Deleted {deleted_branches} branches and {deleted_colleges} colleges")