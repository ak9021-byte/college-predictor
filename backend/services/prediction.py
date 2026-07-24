from db.session import SessionLocal
from models.cutoff import Cutoff
from models.branch import Branch
from models.college import College

def predict_colleges(student_rank: int, category: str):
    db = SessionLocal()

    results = (
        db.query(Cutoff, Branch, College)
        .join(Branch, Cutoff.branch_id == Branch.id)
        .join(College, Branch.college_id == College.id)
        .filter(Cutoff.category == category)
        .filter(Cutoff.closing_rank >= student_rank)
        .all()
    )

    db.close()

    predictions = []
    for cutoff, branch, college in results:
        rank_gap = cutoff.closing_rank - student_rank
        gap_percent = rank_gap / cutoff.closing_rank if cutoff.closing_rank else 0

        if gap_percent > 0.3:
            chance = "High"
        elif gap_percent > 0.1:
            chance = "Moderate"
        else:
            chance = "Low"

        predictions.append({
            "college_name": college.name,
            "branch_name": branch.name,
            "category": cutoff.category,
            "opening_rank": cutoff.opening_rank,
            "closing_rank": cutoff.closing_rank,
            "chance": chance,
        })

    predictions.sort(key=lambda x: x["closing_rank"])
    return predictions

if __name__ == "__main__":
    results = predict_colleges(student_rank=5000, category="GOPENS")
    for r in results:
        print(r)