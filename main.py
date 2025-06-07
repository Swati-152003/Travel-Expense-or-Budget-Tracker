import streamlit as st
import pandas as pd
from expense_logic import add_expense, get_expenses, calculate_summary
import datetime

st.set_page_config(page_title="Travel Expense Tracker", layout="centered")

st.title("🧾 Travel Expense Tracker")

# Input Form
with st.form("expense_form"):
    date = st.date_input("Date", datetime.date.today())
    category = st.selectbox("Category", ["Food", "Travel", "Accommodation", "Shopping", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.5)
    location = st.text_input("Location")
    description = st.text_area("Description")

    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        if amount > 0 and location:
            add_expense({
                "Date": date.strftime("%Y-%m-%d"),
                "Category": category,
                "Amount": amount,
                "Location": location,
                "Description": description
            })
            st.success("Expense added successfully! 💸")
        else:
            st.error("Please fill all required fields.")

# Show Expenses
st.subheader("📊 All Expenses")

df = get_expenses()

if not df.empty:
    # ----------------- 🔍 FILTERS -----------------
    st.markdown("### 🔎 Filter Options")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", df["Date"].min())
    with col2:
        end_date = st.date_input("End Date", df["Date"].max())

    category_filter = st.multiselect(
        "Filter by Category", options=df["Category"].unique().tolist(), default=df["Category"].unique().tolist()
    )

    # Apply filters
    df["Date"] = pd.to_datetime(df["Date"])
    filtered_df = df[
        (df["Date"] >= pd.to_datetime(start_date)) &
        (df["Date"] <= pd.to_datetime(end_date)) &
        (df["Category"].isin(category_filter))
    ]

    st.markdown("### 📋 Filtered Expenses")
    st.dataframe(filtered_df)

    # ----------------- 📊 SUMMARY -----------------
    st.markdown("### 📈 Summary")

    total, summary_df = calculate_summary(filtered_df)
    st.metric("Total Spent (Filtered)", f"₹{total:.2f}")

    st.markdown("#### 💼 Category-wise Breakdown")
    st.dataframe(summary_df)

else:
    st.info("No expenses recorded yet.")
