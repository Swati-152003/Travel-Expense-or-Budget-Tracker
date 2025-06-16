import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, date

def create_metric_box(title, value, subtitle, key):
    """Create a metric box with expandable details"""
    st.markdown(f"""
        <div class="metric-box" onclick="document.getElementById('{key}').click()">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)

def show_total_expenses(expenses):
    """Show total expenses with details"""
    total_spent = expenses['Amount'].sum()
    create_metric_box("💰 TOTAL SPENT", f"₹{total_spent:.2f}", "All Time", "total-details")
    
    with st.expander("📊 View Details", expanded=False):
        st.write("### Total Expenses Details")
        # Distribution pie chart
        fig = px.pie(expenses, values='Amount', names='Category', 
                    title='Total Expenses by Category',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        # Expense table
        st.dataframe(
            expenses.sort_values('Date', ascending=False)[['Date', 'Amount', 'Category', 'Description']],
            hide_index=True,
            use_container_width=True
        )

def show_monthly_expenses(expenses, is_current_month=True):
    """Show monthly expenses with details"""
    current_month = date.today().month
    current_year = date.today().year
    
    if is_current_month:
        month_expenses = expenses[(expenses['Date'].dt.month == current_month) & 
                                (expenses['Date'].dt.year == current_year)]
        title = "📅 THIS MONTH"
        key = "this-month-details"
    else:
        last_month = current_month - 1 if current_month > 1 else 12
        last_month_year = current_year if current_month > 1 else current_year - 1
        month_expenses = expenses[(expenses['Date'].dt.month == last_month) & 
                                (expenses['Date'].dt.year == last_month_year)]
        title = "📅 LAST MONTH"
        key = "last-month-details"
    
    total = month_expenses['Amount'].sum()
    create_metric_box(title, f"₹{total:.2f}", "Expenses", key)
    
    with st.expander("📊 View Details", expanded=False):
        st.write(f"### {'This' if is_current_month else 'Last'} Month's Expenses")
        # Distribution pie chart
        fig = px.pie(month_expenses, values='Amount', names='Category',
                    title=f"{'This' if is_current_month else 'Last'} Month's Expense Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        # Expense table
        st.dataframe(
            month_expenses.sort_values('Date', ascending=False)[['Date', 'Amount', 'Category', 'Description']],
            hide_index=True,
            use_container_width=True
        )

def show_top_category(expenses):
    """Show top category with details"""
    top_category = expenses['Category'].mode()[0]
    top_category_amount = expenses[expenses['Category'] == top_category]['Amount'].sum()
    
    create_metric_box("🏆 TOP CATEGORY", top_category, f"₹{top_category_amount:.2f}", "top-category-details")
    
    with st.expander("📊 View Details", expanded=False):
        st.write(f"### {top_category} Expenses")
        top_category_expenses = expenses[expenses['Category'] == top_category]
        # Distribution pie chart
        fig = px.pie(top_category_expenses, values='Amount', names='Description',
                    title=f'{top_category} Expense Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        # Expense table
        st.dataframe(
            top_category_expenses.sort_values('Date', ascending=False)[['Date', 'Amount', 'Description']],
            hide_index=True,
            use_container_width=True
        )

def show_expense_distribution(expenses):
    """Show overall expense distribution"""
    st.markdown('<div class="distribution-graph">', unsafe_allow_html=True)
    fig = px.pie(expenses, values='Amount', names='Category', 
                title='Overall Expense Distribution',
                color_discrete_sequence=['#800020', '#355E3B', '#1C39BB', '#CD7F32', '#808080', '#FF0000', '#006B54', '#8E4585', '#9400D3', '#9932CC'])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_expense_table(expenses):
    """Show expense table in expander"""
    with st.expander("📋 View Expenses", expanded=False):
        st.markdown('<div class="expense-table">', unsafe_allow_html=True)
        st.dataframe(
            expenses[['Date', 'Amount', 'Category', 'Description']],
            hide_index=True,
            use_container_width=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)

def show_group_expense_details(group_expenses):
    """Show group expense details with distribution graphs"""
    with st.expander("📊 View Details", expanded=False):
        st.write("### Group Expense Details")
        # Distribution pie chart by category
        fig = px.pie(group_expenses, values='Amount', names='Category',
                    title='Group Expenses by Category',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        # Distribution pie chart by spender
        fig_spender = px.pie(group_expenses, values='Amount', names='Spender',
                           title='Group Expenses by Spender',
                           color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_spender, use_container_width=True)
        # Expense table
        st.dataframe(
            group_expenses.sort_values('Date', ascending=False)[['Date', 'Amount', 'Category', 'Description', 'Spender']],
            hide_index=True,
            use_container_width=True
        )

def show_group_monthly_details(group_expenses, is_current_month=True):
    """Show group monthly expense details with distribution graphs"""
    current_month = date.today().month
    current_year = date.today().year
    
    if is_current_month:
        month_expenses = group_expenses[(group_expenses['Date'].dt.month == current_month) & 
                                      (group_expenses['Date'].dt.year == current_year)]
        title = "📅 THIS MONTH"
        key = "group-this-month-details"
    else:
        last_month = current_month - 1 if current_month > 1 else 12
        last_month_year = current_year if current_month > 1 else current_year - 1
        month_expenses = group_expenses[(group_expenses['Date'].dt.month == last_month) & 
                                      (group_expenses['Date'].dt.year == last_month_year)]
        title = "📅 LAST MONTH"
        key = "group-last-month-details"
    
    total = month_expenses['Amount'].sum()
    create_metric_box(title, f"₹{total:.2f}", "Group Expenses", key)
    
    with st.expander("📊 View Details", expanded=False):
        st.write(f"### {'This' if is_current_month else 'Last'} Month's Group Expenses")
        # Distribution pie chart by category
        fig = px.pie(month_expenses, values='Amount', names='Category',
                    title=f"{'This' if is_current_month else 'Last'} Month's Group Expense Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        # Distribution pie chart by spender
        fig_spender = px.pie(month_expenses, values='Amount', names='Spender',
                           title=f"{'This' if is_current_month else 'Last'} Month's Group Expense Distribution by Spender",
                           color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_spender, use_container_width=True)
        # Expense table
        st.dataframe(
            month_expenses.sort_values('Date', ascending=False)[['Date', 'Amount', 'Category', 'Description', 'Spender']],
            hide_index=True,
            use_container_width=True
        )

def show_group_top_category(group_expenses):
    """Show group top category with distribution graph"""
    top_category = group_expenses['Category'].mode()[0]
    top_category_amount = group_expenses[group_expenses['Category'] == top_category]['Amount'].sum()
    
    create_metric_box("🏆 TOP CATEGORY", top_category, f"₹{top_category_amount:.2f}", "group-top-category-details")
    
    with st.expander("📊 View Details", expanded=False):
        st.write(f"### {top_category} Group Expenses")
        top_category_expenses = group_expenses[group_expenses['Category'] == top_category]
        # Distribution pie chart by spender
        fig = px.pie(top_category_expenses, values='Amount', names='Spender',
                    title=f'{top_category} Group Expense Distribution by Spender',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        # Distribution pie chart by description
        fig_desc = px.pie(top_category_expenses, values='Amount', names='Description',
                         title=f'{top_category} Group Expense Distribution by Description',
                         color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_desc, use_container_width=True)
        # Expense table
        st.dataframe(
            top_category_expenses.sort_values('Date', ascending=False)[['Date', 'Amount', 'Description', 'Spender']],
            hide_index=True,
            use_container_width=True
        )

def render_dashboard(expenses):
    """Render the complete dashboard"""
    if not expenses.empty:
        # Convert Date column to datetime
        expenses['Date'] = pd.to_datetime(expenses['Date'])
        
        # Create four columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            show_total_expenses(expenses)
        with col2:
            show_monthly_expenses(expenses, is_current_month=True)
        with col3:
            show_monthly_expenses(expenses, is_current_month=False)
        with col4:
            show_top_category(expenses)
        
        # Show expense distribution
        show_expense_distribution(expenses)
        
        # Show expense table
        show_expense_table(expenses)
        
        # Add some space at the bottom
        st.markdown("<br><br><br><br>", unsafe_allow_html=True) 