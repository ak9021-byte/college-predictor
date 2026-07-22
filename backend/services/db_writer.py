from db.session import SessionLocal
from models.college import College
from models.branch import Branch
from services.excel_importer import read_and_clean_seat_matrix
import pandas as pd

def write_seat_data_to_db(file_path):
    data = read_and_clean_seat_matrix(file_path)
    db = SessionLocal()

    colleges_created = 0
    branches_created = 0
    skipped_rows = 0

    for _, row in data.iterrows():
        # Skip rows with missing/invalid seat counts
        if pd.isna(row["seats"]):
            skipped_rows += 1
            continue

        try:
            seat_count = int(row["seats"])
        except (ValueError, TypeError):
            skipped_rows += 1
            continue

        # Get or create the college
        college = db.query(College).filter_by(name=row["college_name"]).first()
        if not college:
            college = College(code=row["college_code"], name=row["college_name"])
            db.add(college)
            db.commit()
            db.refresh(college)
            colleges_created += 1

        # Get or create the branch under that college
        branch = db.query(Branch).filter_by(
            name=row["branch"], college_id=college.id
        ).first()
        if not branch:
            branch = Branch(
                name=row["branch"],
                college_id=college.id,
                capacity=seat_count
            )
            db.add(branch)
            db.commit()
            branches_created += 1

    db.close()
    print(f"Done. Colleges created: {colleges_created}, Branches created: {branches_created}, Rows skipped (bad data): {skipped_rows}")

if __name__ == "__main__":
    write_seat_data_to_db("data/Seats.xlsx")