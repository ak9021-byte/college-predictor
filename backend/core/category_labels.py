CATEGORY_LABELS = {}

PREFIX_LABELS = {"G": "General", "L": "Ladies", "DEF": "Defense", "PWD": "PWD", "DEFR": "Defense (Reserved)", "PWDR": "PWD (Reserved)"}
CATEGORY_NAMES = {"OPEN": "Open", "SC": "SC", "ST": "ST", "VJ": "VJ/DT", "NT1": "NT-B", "NT2": "NT-C", "NT3": "NT-D", "OBC": "OBC", "SEBC": "SEBC"}
SUFFIX_LABELS = {"S": "State Level", "H": "Home University", "O": "Other Home University"}

import re

def build_label(code):
    if code in ("EWS", "TFWS", "MI", "ORPHAN"):
        return {"EWS": "EWS", "TFWS": "TFWS (Fee Waiver)", "MI": "Minority", "ORPHAN": "Orphan"}[code]

    match = re.match(r"^(G|L|DEFR|PWDR|DEF|PWD)(OPEN|SC|ST|VJ|NT1|NT2|NT3|OBC|SEBC)(S|H|O)?$", code)
    if not match:
        return code

    prefix, category, suffix = match.groups()
    label = f"{CATEGORY_NAMES.get(category, category)} ({PREFIX_LABELS.get(prefix, prefix)})"
    if suffix:
        label += f" - {SUFFIX_LABELS.get(suffix, suffix)}"
    return label

ALL_CATEGORIES = [
    "DEFOBCS","DEFOPENS","DEFRNT1S","DEFRNT2S","DEFRNT3S","DEFROBCS","DEFRSCS","DEFRSEBCS","DEFRSTS","DEFRVJS",
    "DEFSCS","DEFSEBCS","DEFSTS","EWS","GNT1H","GNT1O","GNT1S","GNT2H","GNT2O","GNT2S","GNT3H","GNT3O","GNT3S",
    "GOBCH","GOBCO","GOBCS","GOPENH","GOPENO","GOPENS","GSCH","GSCO","GSCS","GSEBCH","GSEBCO","GSEBCS","GSTH",
    "GSTO","GSTS","GVJH","GVJO","GVJS","LNT1H","LNT1O","LNT1S","LNT2H","LNT2O","LNT2S","LNT3H","LNT3O","LNT3S",
    "LOBCH","LOBCO","LOBCS","LOPENH","LOPENO","LOPENS","LSCH","LSCO","LSCS","LSEBCH","LSEBCO","LSEBCS","LSTH",
    "LSTO","LSTS","LVJH","LVJO","LVJS","MI","ORPHAN","PWDOBCH","PWDOBCS","PWDOPENH","PWDOPENS","PWDRNT1S",
    "PWDRNT2S","PWDRNT3S","PWDROBCH","PWDROBCS","PWDRSCH","PWDRSCS","PWDRSEBCS","PWDRSTS","PWDRVJS","PWDSCS",
    "PWDSEBCS","PWDSTS","TFWS"
]

CATEGORY_LABELS = {code: build_label(code) for code in ALL_CATEGORIES}