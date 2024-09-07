-- Create trip_expenses table
CREATE TABLE IF NOT EXISTS trip_expenses (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    location TEXT NOT NULL
);

-- Create places table (unchanged)
CREATE TABLE IF NOT EXISTS places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lat DECIMAL(9, 6) NOT NULL,
    lon DECIMAL(9, 6) NOT NULL,
    spent DECIMAL(10, 2) NOT NULL
);

-- Create favorite_foods table (unchanged)
CREATE TABLE IF NOT EXISTS favorite_foods (
    id SERIAL PRIMARY KEY,
    food_name VARCHAR(100) NOT NULL
);
