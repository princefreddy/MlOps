CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    input_data TEXT NOT NULL,
    prediction TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);