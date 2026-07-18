import pandas as pd
from db.session import SessionLocal
from models.college import College

def update_college_info(file_path):
    df = pd.read_excel(file_path, sheet_name="Sheet1")
    db = SessionLocal()

    updated = 0
    not_found = 0

    for _, row in df.iterrows():
        institute_code = row["Institute Code "]
        if pd.isna(institute_code):
            continue

        # normalize: Seats.xlsx stored codes like "01002", this file has 1002.0
        code_str = str(int(institute_code)).zfill(5)

        college = db.query(College).filter_by(code=code_str).first()
        if not college:
            not_found += 1
            continue

        college.status = row.get("Status ")
        college.established = str(row.get("Established ")) if pd.notna(row.get("Established ")) else None
        college.website = row.get("Official website")
        college.place = row.get("Place ")
        college.naac_rating = row.get("NAAC Rating ")
        college.fees = row.get("Fees ")
        college.hostel_available = row.get("Hostel Y/N ")
        college.students_placed_last_year = (
            int(row["How many students got placed last year ? "])
            if pd.notna(row.get("How many students got placed last year ? "))
            else None
        )
        college.highest_package = row.get("Highesht package ? ")
        college.average_package = row.get("Average package ? ")
        college.companies_visited = (
            int(row["No of compnies visited for placement "])
            if pd.notna(row.get("No of compnies visited for placement "))
            else None
        )
        updated += 1

    db.commit()
    db.close()
    print(f"Updated: {updated}, Not matched to existing college: {not_found}")

if __name__ == "__main__":
    update_college_info("data/Master Data - Engineering .xlsx")