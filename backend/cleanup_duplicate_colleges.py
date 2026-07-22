import re
from sqlalchemy import text
from db.session import SessionLocal
from models.college import College
from models.branch import Branch

def cleanup_duplicate_colleges():
    db = SessionLocal()

    duplicates = db.execute(text("""
        SELECT name, array_agg(id ORDER BY id) as ids, array_agg(code ORDER BY id) as codes
        FROM colleges
        GROUP BY name
        HAVING COUNT(*) > 1
    """)).fetchall()

    print(f"Found {len(duplicates)} duplicate college name groups")

    merged_branches = 0
    deleted_colleges = 0
    proper_code_pattern = re.compile(r"^\d{5}$")

    for row in duplicates:
        ids = row.ids
        codes = row.codes

        keep_id = None
        for cid, code in zip(ids, codes):
            if code and proper_code_pattern.match(code):
                keep_id = cid
                break
        if keep_id is None:
            keep_id = ids[0]

        remove_ids = [i for i in ids if i != keep_id]

        for remove_id in remove_ids:
            moved = db.query(Branch).filter_by(college_id=remove_id).update(
                {"college_id": keep_id}
            )
            merged_branches += moved

            db.query(College).filter_by(id=remove_id).delete()
            deleted_colleges += 1

    db.commit()
    db.close()
    print(f"Re-linked {merged_branches} branches to the correct college")
    print(f"Deleted {deleted_colleges} duplicate college rows")

if __name__ == "__main__":
    cleanup_duplicate_colleges()