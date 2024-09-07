-- Create trip_expenses table
CREATE TABLE IF NOT EXISTS trip_expenses (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    expense_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL
);

-- Create places table
CREATE TABLE IF NOT EXISTS places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lat DECIMAL(9, 6) NOT NULL,
    lon DECIMAL(9, 6) NOT NULL,
    spent DECIMAL(10, 2) NOT NULL
);

-- Create favorite_foods table
CREATE TABLE IF NOT EXISTS favorite_foods (
    id SERIAL PRIMARY KEY,
    food_name VARCHAR(100) NOT NULL
);
