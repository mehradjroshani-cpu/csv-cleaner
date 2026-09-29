# CSV Cleaner

A Python script that cleans messy customer data in CSV files.

## What it does
- Trims extra spaces and fixes name/product/region capitalization
- Lowercases emails
- Standardizes phone numbers to (555) 123-4567 and flags invalid ones
- Converts prices like "$1,045.00" into numbers
- Flags duplicate emails and calculates line totals

## How to use
1. Install pandas: `pip install pandas`
2. Run:
   python csv_cleaner.py messy_sample.csv cleaned.csv

## Example
The included `messy_sample.csv` has 15 rows of fictional data. The script finds 2 duplicates and 1 invalid phone number.

## Built with
Python, pandas
