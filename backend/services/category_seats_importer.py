import pandas as pd
from db.session import SessionLocal
from models.college import College
from models.branch import Branch
from models.category_seat import CategorySeat

CATEGORIES = ["OPEN", "SC", "ST", "VJ_DT", "NTB", "NTC", "NTD", "OBC", "SEBC"]

def import_category_seats(file_path):
    df = pd.read_excel(file_path, sheet_name="Seat Matrix (All Courses)")
    db = SessionLocal()

    created = 0
    skipped_no_college = 0
    branches_created = 0
    skipped_duplicate = 0

    for _, row in df.iterrows():
        college_code = str(int(row["College Code"])).zfill(5)
        branch_name = str(row["Department / Course"]).strip().title()
        choice_code = str(row["Choice Code"])

        college = db.query(College).filter_by(code=college_code).first()
        if not college:
            skipped_no_college += 1
            continue

        branch = db.query(Branch).filter_by(
            name=branch_name, college_id=college.id
        ).first()
        if not branch:
            total_seats = row.get("Total Seats (Sanctioned Intake)", 0)
            total_seats = int(total_seats) if pd.notna(total_seats) else 0
            branch = Branch(name=branch_name, college_id=college.id, capacity=total_seats)
            db.add(branch)
            db.commit()
            db.refresh(branch)
            branches_created += 1

        pwd = row.get("PWD Seats (within above, horizontal reservation)", 0)
        defence = row.get("Defence (DEF) Seats (within above, horizontal reservation)", 0)
        ews = row.get("EWS Seats (separate, economically weaker section)", 0)
        tfws = row.get("TFWS Seats (extra, fee-waiver only)", 0)
        pwd = int(pwd) if pd.notna(pwd) else 0
        defence = int(defence) if pd.notna(defence) else 0
        ews = int(ews) if pd.notna(ews) else 0
        tfws = int(tfws) if pd.notna(tfws) else 0

        for cat in CATEGORIES:
            general = row.get(f"{cat} - General", 0)
            ladies = row.get(f"{cat} - Ladies", 0)
            general = int(general) if pd.notna(general) else 0
            ladies = int(ladies) if pd.notna(ladies) else 0

            existing = db.query(CategorySeat).filter_by(
                branch_id=branch.id, category=cat, choice_code=choice_code
            ).first()
            if existing:
                skipped_duplicate += 1
                continue

            cat_seat = CategorySeat(
                branch_id=branch.id,
                choice_code=choice_code,
                category=cat,
                general_seats=general,
                ladies_seats=ladies,
                total_seats=general + ladies,
                pwd_seats=pwd,
                def_seats=defence,
                ews_seats=ews,
                tfws_seats=tfws,
            )
            db.add(cat_seat)
            created += 1

    db.commit()
    db.close()
    print(f"Created: {created}")
    print(f"Skipped (college not found): {skipped_no_college}")
    print(f"New branches created: {branches_created}")
    print(f"Skipped (already existed): {skipped_duplicate}")

if __name__ == "__main__":
    import_category_seats("data/Seat_Matrix.xlsx")