-- Seed trip_expenses table
INSERT INTO trip_expenses (city, expense_type, amount, date) VALUES
('Paris', 'Food', 150.00, '2023-06-01'),
('Paris', 'Accommodation', 200.00, '2023-06-01'),
('Rome', 'Transportation', 50.00, '2023-06-05'),
('Rome', 'Activities', 100.00, '2023-06-06'),
('Barcelona', 'Food', 80.00, '2023-06-10'),
('Amsterdam', 'Accommodation', 180.00, '2023-06-15');

-- Seed places table
INSERT INTO places (name, lat, lon, spent) VALUES
('Paris', 48.8566, 2.3522, 1500),
('Rome', 41.9028, 12.4964, 1200),
('Barcelona', 41.3851, 2.1734, 1000),
('Amsterdam', 52.3676, 4.9041, 800);

-- Seed favorite_foods table
INSERT INTO favorite_foods (food_name) VALUES
('Croissant'),
('Pizza'),
('Paella'),
('Stroopwafel');
