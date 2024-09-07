import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import os

# Assuming DB_URL is set in your Streamlit secrets
DB_URL = st.secrets["DB_URL"]
engine = create_engine(DB_URL)

def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

def execute_query(query):
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()

def read_sql_file(filename):
    with open(os.path.join('database', filename), 'r') as file:
        return file.read()

def reset_database():
    # Drop existing tables
    execute_query("DROP TABLE IF EXISTS trip_expenses, places, favorite_foods;")
    
    # Create tables
    create_tables_sql = read_sql_file('create_tables.sql')
    execute_query(create_tables_sql)
    
    # Seed data
    seed_data_sql = read_sql_file('seed_data.sql')
    execute_query(seed_data_sql)

st.title("Europe Trip Data")

# Admin Section
st.sidebar.header("Admin Section")
if st.sidebar.button("Reset Database to Initial State"):
    if st.sidebar.button("Are you sure? This will delete all current data."):
        try:
            reset_database()
            st.sidebar.success("Database reset successfully!")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")

# Rest of your Streamlit app code...

# Expenses
st.header("Trip Expenses")
expenses_query = "SELECT * FROM trip_expenses ORDER BY date"
expenses_df = run_query(expenses_query)
st.dataframe(expenses_df)

# Expense by type pie chart
st.subheader("Expenses by Type")
expense_by_type = expenses_df.groupby('expense_type')['amount'].sum().reset_index()
fig = px.pie(expense_by_type, values='amount', names='expense_type', title='Expense Distribution')
st.plotly_chart(fig)

# Places visited
st.header("Places Visited")
places_query = "SELECT * FROM places"
places_df = run_query(places_query)
st.map(places_df)

# Bar chart of spending by place
fig = px.bar(places_df, x='name', y='spent', title='Spending by Place')
st.plotly_chart(fig)

# Favorite Foods
st.header("Favorite Foods")
foods_query = "SELECT * FROM favorite_foods"
foods_df = run_query(foods_query)
st.write(foods_df['food_name'].tolist())

# Total Spending
total_spent = expenses_df['amount'].sum()
st.metric("Total Trip Expenses", f"€{total_spent:.2f}")
