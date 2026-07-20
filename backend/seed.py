from passlib.context import CryptContext
from db.session import SessionLocal
from models.exam import Exam
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    db = SessionLocal()

    # Seed the exam
    existing_exam = db.query(Exam).filter_by(name="MHT-CET").first()
    if not existing_exam:
        exam = Exam(name="MHT-CET")
        db.add(exam)
        print("Created exam: MHT-CET")
    else:
        print("Exam already exists: MHT-CET")

    # Seed one admin user
    existing_admin = db.query(User).filter_by(email="admin@collegepredictor.com").first()
    if not existing_admin:
        hashed_password = pwd_context.hash("ChangeThisPassword123")
        admin = User(
            email="admin@collegepredictor.com",
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin)
        print("Created admin user: admin@collegepredictor.com")
    else:
        print("Admin user already exists")

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()