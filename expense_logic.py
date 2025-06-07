from sheets_service import connect_to_sheet
import pandas as pd

HEADERS = ["Date", "Category", "Amount", "Location", "Description"]

def add_expense(expense: dict):
    sheet = connect_to_sheet()
    # Make sure headers exist
    if sheet.row_count == 0 or sheet.row_values(1) != HEADERS:
        sheet.insert_row(HEADERS, 1)

    values = [expense.get(h, "") for h in HEADERS]
    sheet.append_row(values)

def get_expenses():
    sheet = connect_to_sheet()
    records = sheet.get_all_records()
    return pd.DataFrame(records)

def calculate_summary(df: pd.DataFrame):
    total = df["Amount"].sum() if not df.empty else 0
    by_category = df.groupby("Category")["Amount"].sum().reset_index()
    return total, by_category
