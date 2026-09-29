"""
CSV Cleaner - a small tool that tidies messy customer data.

Usage:
    python csv_cleaner.py input.csv output.csv

Expected columns: Name, Email, Phone, Product, Qty, Unit Price, Region
What it does:
  - trims extra spaces and fixes name/product/region capitalization
  - lowercases emails
  - standardizes phone numbers to (555) 123-4567 (flags invalid ones)
  - converts prices like "$1,045.00" to numbers
  - flags duplicate emails and calculates line totals
"""
import re
import sys
import pandas as pd


def clean_phone(value):
    digits = re.sub(r"\D", "", str(value))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return "INVALID"


def clean(df):
    out = pd.DataFrame()
    out["Name"] = df["Name"].str.split().str.join(" ").str.title()
    out["Email"] = df["Email"].str.strip().str.lower()
    out["Phone"] = df["Phone"].apply(clean_phone)
    out["Product"] = df["Product"].str.split().str.join(" ").str.title().str.replace("Usb", "USB")
    out["Qty"] = df["Qty"].astype(int)
    out["Unit Price"] = (
        df["Unit Price"].astype(str).str.replace(r"[$,]", "", regex=True).astype(float)
    )
    out["Line Total"] = out["Qty"] * out["Unit Price"]
    out["Region"] = df["Region"].str.strip().str.title()
    out["Duplicate"] = out.duplicated(subset="Email", keep="first")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python csv_cleaner.py input.csv output.csv")
    cleaned = clean(pd.read_csv(sys.argv[1]))
    cleaned.to_csv(sys.argv[2], index=False)
    print(f"Cleaned {len(cleaned)} rows -> {sys.argv[2]}")
    print(f"Duplicates flagged: {cleaned['Duplicate'].sum()}")
    print(f"Invalid phones: {(cleaned['Phone'] == 'INVALID').sum()}")
