import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text, exc
import plotly.express as px
import os
from datetime import datetime, timedelta

# Assuming DB_URL is set in your Streamlit secrets
DB_URL = st.secrets["DB_URL"]
engine = create_engine(DB_URL)

def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

def execute_query(query, params=None):
    with engine.connect() as conn:
        conn.execute(text(query), params)
        conn.commit()

def read_sql_file(filename):
    with open(os.path.join('database', filename), 'r') as file:
        return file.read()

def reset_database():
    create_tables_sql = read_sql_file('create_tables.sql')
    seed_data_sql = read_sql_file('seed_data.sql')
    execute_query(create_tables_sql)
    execute_query(seed_data_sql)

def check_tables_exist():
    try:
        run_query("SELECT 1 FROM trip_expenses LIMIT 1")
        return True
    except exc.ProgrammingError:
        return False

st.title("Europe Trip Expense Tracker")

# Check if tables exist
tables_exist = check_tables_exist()

# Sidebar for database operations
st.sidebar.header("Database Operations")
if not tables_exist:
    st.sidebar.warning("Database tables do not exist. Please initialize the database.")
    if st.sidebar.button("Initialize Database"):
        try:
            reset_database()
            st.sidebar.success("Database initialized successfully!")
            tables_exist = True
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")
else:
    if st.sidebar.button("Reset Database"):
        if st.sidebar.button("Are you sure? This will delete all current data."):
            try:
                reset_database()
                st.sidebar.success("Database reset successfully!")
            except Exception as e:
                st.sidebar.error(f"An error occurred: {e}")

# Main content
if tables_exist:
    # Collapsible input form for new expense
    with st.expander("Add New Expense"):
        with st.form("new_expense_form"):
            user_id = st.text_input("User ID")
            price = st.number_input("Price", min_value=0.01, step=0.01)
            date = st.date_input("Date")
            time = st.time_input("Time")
            description = st.text_input("Description")
            category = st.selectbox("Category", ["Food", "Accommodation", "Transportation", "Activities", "Other"])
            location = st.text_input("Location (Address)")
            
            submit_button = st.form_submit_button("Add Expense")
            
            if submit_button:
                datetime_str = f"{date} {time}"
                query = """
                INSERT INTO trip_expenses (user_id, price, datetime, description, category, location)
                VALUES (:user_id, :price, :datetime, :description, :category, :location)
                """
                try:
                    execute_query(query, {
                        "user_id": user_id,
                        "price": price,
                        "datetime": datetime_str,
                        "description": description,
                        "category": category,
                        "location": location
                    })
                    st.success("Expense added successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Display expenses
    st.header("Trip Expenses")
    expenses_query = """
    SELECT user_id, price, datetime, description, category, location 
    FROM trip_expenses 
    ORDER BY datetime DESC
    """
    expenses_df = run_query(expenses_query)
    expenses_df['datetime'] = pd.to_datetime(expenses_df['datetime'])
    st.dataframe(expenses_df)

    # Expense analysis
    st.header("Expense Analysis")

    # Total spending
    total_spent = expenses_df['price'].sum()
    st.metric("Total Trip Expenses", f"€{total_spent:.2f}")

    # Spending by category
    category_expenses = expenses_df.groupby('category')['price'].sum().reset_index()
    fig = px.bar(category_expenses, y='category', x='price', title='Expenses by Category', orientation='h')
    st.plotly_chart(fig)

    # Spending over time
    expenses_df['date'] = expenses_df['datetime'].dt.date
    daily_expenses = expenses_df.groupby('date')['price'].sum().reset_index()
    fig = px.line(daily_expenses, x='date', y='price', title='Daily Expenses')
    st.plotly_chart(fig)

    # Top 5 most expensive items
    st.subheader("Top 5 Most Expensive Items")
    top_expenses = expenses_df.nlargest(5, 'price')
    st.table(top_expenses[['description', 'price', 'category', 'datetime']])

    # Expenses by user
    user_expenses = expenses_df.groupby('user_id')['price'].sum().reset_index()
    fig = px.bar(user_expenses, x='user_id', y='price', title='Expenses by User')
    st.plotly_chart(fig)

else:
    st.info("Please initialize the database using the button in the sidebar to view and add expenses.")
