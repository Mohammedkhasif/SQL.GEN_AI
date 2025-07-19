DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT,
    age INTEGER
);

INSERT INTO customers (name, city, age) VALUES
('Ayesha', 'Mumbai', 25),
('Rahul', 'Delhi', 32),
('Karan', 'Bangalore', 28),
('Bushra', 'Hyderabad', 26);
