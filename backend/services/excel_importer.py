import pandas as pd
import re

def split_code_and_name(college_name_and_code):
    """
    Splits '3013 - Veermata Jijabai Technological Institute(VJTI), Matunga, Mumbai'
    into code='3013' and name='Veermata Jijabai Technological Institute(VJTI), Matunga, Mumbai'
    """
    if pd.isna(college_name_and_code):
        return None, None
    match = re.match(r"^\s*(\S+)\s*-\s*(.+)$", str(college_name_and_code))
    if match:
        code = match.group(1).strip()
        name = match.group(2).strip()
        return code, name
    return None, str(college_name_and_code).strip()

def read_and_clean_seat_matrix(file_path):
    xl = pd.ExcelFile(file_path)
    all_rows = []

    for sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet_name)

        expected_cols = {"sr no", "college name & code", "branch", "seats"}
        if not expected_cols.issubset(set(df.columns)):
            continue

        df = df[df["branch"].astype(str).str.strip().str.lower() != "total"]
        df = df.dropna(subset=["college name & code"])

        codes_and_names = df["college name & code"].apply(split_code_and_name)
        df["college_code"] = [c[0] for c in codes_and_names]
        df["college_name"] = [c[1] for c in codes_and_names]

        df["branch"] = df["branch"].astype(str).str.strip().str.title()

        all_rows.append(df[["college_code", "college_name", "branch", "seats"]])

    combined = pd.concat(all_rows, ignore_index=True)
    combined = combined.drop_duplicates()
    return combined

if __name__ == "__main__":
    data = read_and_clean_seat_matrix("data/Seats.xlsx")
    print(f"Total rows: {len(data)}")
    print(data.head(20))