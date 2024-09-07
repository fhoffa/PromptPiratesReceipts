import os
from sqlalchemy import create_engine, text
from datetime import datetime

# Replace with your actual Neon database URL
DB_URL = os.environ.get('NEON_DB_URL', 'postgresql://user:password@host:port/database')

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

def insert_expense(user_id, price, datetime, description, category, location):
    query = text("""
    INSERT INTO trip_expenses (user_id, price, datetime, description, category, location)
    VALUES (:user_id, :price, :datetime, :description, :category, :location)
    """)
    
    with engine.connect() as conn:
        conn.execute(query, {
            "user_id": user_id,
            "price": price,
            "datetime": datetime,
            "description": description,
            "category": category,
            "location": location
        })
        conn.commit()

# Example usage
if __name__ == "__main__":
    try:
        insert_expense(
            user_id="alice",
            price=42.50,
            datetime=datetime.now(),
            description="Dinner at Local Restaurant",
            category="Food",
            location="123 Main St, City, Country"
        )
        print("Expense inserted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
