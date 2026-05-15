CREATE TABLE users (email VARCHAR(255) PRIMARY KEY,password VARCHAR(255));
CREATE TABLE sessions (token VARCHAR(255) PRIMARY KEY, email VARCHAR(255),expires_at FLOAT);
CREATE TABLE transactions (id SERIAL PRIMARY KEY, user_email VARCHAR(255), amount FLOAT,currency VARCHAR(50), merchant VARCHAR(255),time FLOAT);
CREATE TABLE attempts (ip VARCHAR(50), time FLOAT);