-- Seed trip_expenses table
INSERT INTO trip_expenses (user_id, price, datetime, description, category, location) VALUES
('alice', 25.50, '2023-06-01 12:30:00+02:00', 'Lunch at Café de Flore', 'Food', '172 Boulevard Saint-Germain, 75006 Paris, France'),
('alice', 150.00, '2023-06-01 15:00:00+02:00', 'Louvre Museum tickets', 'Activities', 'Rue de Rivoli, 75001 Paris, France'),
('bob', 80.00, '2023-06-02 20:00:00+02:00', 'Dinner at La Pizzeria', 'Food', 'Via della Croce 8, 00187 Rome, Italy'),
('alice', 200.00, '2023-06-03 10:00:00+02:00', 'Hotel Splendide Royal', 'Accommodation', 'Via di Porta Pinciana 14, 00187 Rome, Italy'),
('bob', 15.00, '2023-06-04 14:30:00+02:00', 'Gelato at Giolitti', 'Food', 'Via degli Uffici del Vicario 40, 00186 Rome, Italy'),
('alice', 50.00, '2023-06-05 09:00:00+02:00', 'Taxi to Vatican City', 'Transportation', 'Piazza San Pietro, 00120 Città del Vaticano, Vatican City'),
('bob', 120.00, '2023-06-06 11:00:00+02:00', 'Sagrada Familia tour', 'Activities', 'Carrer de Mallorca 401, 08013 Barcelona, Spain'),
('alice', 30.00, '2023-06-07 13:00:00+02:00', 'Tapas at La Boqueria', 'Food', 'La Rambla 91, 08001 Barcelona, Spain'),
('bob', 180.00, '2023-06-08 16:00:00+02:00', 'Hotel Casa Fuster', 'Accommodation', 'Passeig de Gràcia 132, 08008 Barcelona, Spain'),
('alice', 40.00, '2023-06-09 10:00:00+02:00', 'Canal tour', 'Activities', 'Prins Hendrikkade 33A, 1012 TM Amsterdam, Netherlands'),
('bob', 18.00, '2023-06-10 15:30:00+02:00', 'Stroopwafels at Albert Cuyp Market', 'Food', 'Albert Cuypstraat, 1073 BD Amsterdam, Netherlands');

-- Seed places table (unchanged)
INSERT INTO places (name, lat, lon, spent) VALUES
('Paris', 48.8566, 2.3522, 1500),
('Rome', 41.9028, 12.4964, 1200),
('Barcelona', 41.3851, 2.1734, 1000),
('Amsterdam', 52.3676, 4.9041, 800);

-- Seed favorite_foods table (unchanged)
INSERT INTO favorite_foods (food_name) VALUES
('Croissant'),
('Pizza'),
('Paella'),
('Stroopwafel');
