import re
import pdfplumber
from db.session import SessionLocal
from models.college import College
from models.branch import Branch
from models.category_seat import CategorySeat

CATEGORIES = ["OPEN", "SC", "ST", "VJ/DT", "NTB", "NTC", "NTD", "OBC", "SEBC"]

college_re = re.compile(r'^(\d+)\s*-\s*(.+)$', re.MULTILINE)
choice_re = re.compile(r'^\s*(\d{10}[A-Z]{0,2})\s+(.+?)\s{2,}\d', re.MULTILINE)
row_re = re.compile(r'^\s*(State Level|HU|OHU)\s+((?:\d+\s+){18}\d+)\s*$', re.MULTILINE)


def extract_text(pdf_path):
    """
    Extract text from the seat matrix PDF using pdfplumber (pure Python,
    no external 'pdftotext' binary required). Pages are joined with a
    form-feed character (\\f) to match the page-splitting logic in
    parse_pages(), which previously relied on pdftotext's own page breaks.
    """
    text_chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"PDF opened: {total} pages found. Extracting...")
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text(layout=True) or ""
            text_chunks.append(page_text)
            if i % 10 == 0 or i == total:
                print(f"  processed page {i}/{total}")
    return "\f".join(text_chunks)


def parse_pages(text):
    pages = [p for p in text.split('\f') if p.strip()]
    records = []

    for page in pages:
        college_match = college_re.search(page)
        choice_match = choice_re.search(page)
        rows = row_re.findall(page)

        if not (college_match and choice_match and rows):
            continue

        college_code = college_match.group(1).strip()
        choice_code, branch_name = choice_match.groups()

        # sum all seat rows (State Level, or HU + OHU) into one total per category
        totals = [0] * 19
        for _, numbers_str in rows:
            nums = [int(n) for n in numbers_str.split()]
            totals = [a + b for a, b in zip(totals, nums)]

        for i, cat in enumerate(CATEGORIES):
            general = totals[i * 2]
            ladies = totals[i * 2 + 1]
            records.append({
                "college_code": college_code,
                "choice_code": choice_code,
                "branch_name": branch_name.strip(),
                "category": cat,
                "general_seats": general,
                "ladies_seats": ladies,
                "total_seats": general + ladies,
            })

    return records


def write_to_db(records):
    db = SessionLocal()
    created = 0
    skipped = 0

    for r in records:
        college = db.query(College).filter_by(code=r["college_code"]).first()
        if not college:
            skipped += 1
            continue

        branch = db.query(Branch).filter_by(
            name=r["branch_name"], college_id=college.id
        ).first()
        if not branch:
            skipped += 1
            continue

        existing = db.query(CategorySeat).filter_by(
            branch_id=branch.id, category=r["category"], choice_code=r["choice_code"]
        ).first()
        if existing:
            continue

        cat_seat = CategorySeat(
            branch_id=branch.id,
            choice_code=r["choice_code"],
            category=r["category"],
            general_seats=r["general_seats"],
            ladies_seats=r["ladies_seats"],
            total_seats=r["total_seats"],
        )
        db.add(cat_seat)
        created += 1

    db.commit()
    db.close()
    print(f"Created: {created}, Skipped (no matching college/branch): {skipped}")


if __name__ == "__main__":
    text = extract_text("data/Seat_Matrix_Engineering_2025.pdf")
    records = parse_pages(text)
    print(f"Parsed {len(records)} category-seat records from PDF")
    write_to_db(records)