import time
import pdfplumber

PDF_PATH = "data/Seat_Matrix_Engineering_2025.pdf"
START_PAGE = 2120  # 0-indexed area near where it got stuck

with pdfplumber.open(PDF_PATH) as pdf:
    total = len(pdf.pages)
    for i, page in enumerate(pdf.pages, start=1):
        if i < START_PAGE:
            continue
        t0 = time.time()
        _ = page.extract_text(layout=True) or ""
        elapsed = time.time() - t0
        print(f"page {i}/{total}: {elapsed:.2f}s")
        if elapsed > 5:
            print(f"  >>> SLOW PAGE FOUND: {i} took {elapsed:.2f}s")