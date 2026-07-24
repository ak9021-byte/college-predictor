import re
import pandas as pd
from sqlalchemy import func
from db.session import SessionLocal
from models.college import College
from models.branch import Branch
from models.cutoff import Cutoff

CELL_PATTERN = re.compile(r'^(\d+)\s*\(([\d.]+)%\)$')
STAGE_MAP = {"I": 1, "II": 2, "III": 3}

METADATA_COLS = {"Sr No", "college_code", "college_name", "dept_code", "dept_name", "status", "level", "stage"}

def parse_cell(value):
    if pd.isna(value):
        return None, None
    match = CELL_PATTERN.match(str(value).strip())
    if not match:
        return None, None
    return int(match.group(1)), float(match.group(2))

def import_cutoffs(file_path, year=2025):
    df = pd.read_excel(file_path, sheet_name="Sheet1")
    category_cols = [c for c in df.columns if c not in METADATA_COLS]

    db = SessionLocal()

    created = 0
    skipped_no_college = 0
    skipped_no_branch = 0
    college_cache = {}
    branch_cache = {}

    for idx, row in df.iterrows():
        college_name_raw = str(row["college_name"]).strip()
        branch_name_raw = str(row["dept_name"]).strip()
        round_num = STAGE_MAP.get(str(row["stage"]).strip(), None)
        level = row.get("level")

        college_key = college_name_raw.lower()
        if college_key not in college_cache:
            college_cache[college_key] = db.query(College).filter(
                func.lower(College.name) == college_key
            ).first()
        college = college_cache[college_key]
        if not college:
            skipped_no_college += 1
            continue

        branch_key = (college.id, branch_name_raw.lower())
        if branch_key not in branch_cache:
            branch_cache[branch_key] = db.query(Branch).filter(
                Branch.college_id == college.id,
                func.lower(Branch.name) == branch_name_raw.lower()
            ).first()
        branch = branch_cache[branch_key]
        if not branch:
            skipped_no_branch += 1
            continue

        for col in category_cols:
            rank, percentile = parse_cell(row[col])
            if rank is None:
                continue

            cutoff = Cutoff(
                branch_id=branch.id,
                category=col,
                level=level,
                round=round_num,
                year=year,
                closing_rank=rank,
                percentile=percentile,
            )
            db.add(cutoff)
            created += 1

        if idx % 500 == 0:
            db.commit()
            print(f"...processed {idx} rows, {created} cutoffs created so far")

    db.commit()
    db.close()
    print(f"Done. Created: {created}")
    print(f"Skipped (college not found): {skipped_no_college}")
    print(f"Skipped (branch not found): {skipped_no_branch}")

if __name__ == "__main__":
    import_cutoffs("data/Cutoffs_2025.xlsx")