from sqlalchemy import text
from db.session import SessionLocal
from models.branch import Branch
from models.category_seat import CategorySeat

def cleanup_duplicates():
    db = SessionLocal()

    # find all (college_id, name) combos that have duplicates
    duplicates = db.execute(text("""
        SELECT college_id, name, array_agg(id ORDER BY id) as ids
        FROM branches
        GROUP BY college_id, name
        HAVING COUNT(*) > 1
    """)).fetchall()

    print(f"Found {len(duplicates)} duplicate branch groups")

    merged = 0
    deleted = 0

    for row in duplicates:
        ids = row.ids
        keep_id = ids[0]           # keep the first (oldest) one
        remove_ids = ids[1:]       # merge and delete the rest

        for remove_id in remove_ids:
            # move any category_seats pointing to the duplicate over to the kept branch
            moved = db.query(CategorySeat).filter_by(branch_id=remove_id).update(
                {"branch_id": keep_id}
            )
            merged += moved

            # now safe to delete the duplicate branch
            db.query(Branch).filter_by(id=remove_id).delete()
            deleted += 1

    db.commit()
    db.close()
    print(f"Merged {merged} category_seat rows onto kept branches")
    print(f"Deleted {deleted} duplicate branch rows")

if __name__ == "__main__":
    cleanup_duplicates()