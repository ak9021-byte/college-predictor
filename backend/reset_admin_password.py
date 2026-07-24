from passlib.context import CryptContext
from db.session import SessionLocal
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()
admin = db.query(User).filter_by(email="admin@collegepredictor.com").first()

if admin:
    new_password = "Admin@2026"  # change this to whatever you want
    admin.hashed_password = pwd_context.hash(new_password)
    db.commit()
    print(f"Password reset successfully for {admin.email}")
else:
    print("Admin user not found")

db.close()