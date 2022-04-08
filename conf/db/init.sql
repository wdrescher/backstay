CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE users (
    user_id int PRIMARY KEY,
    email varchar(100) UNIQUE NOT NULL, 
    password varchar(30) not NULL,
    phone_number varchar(10), 
    first_name varchar(50), 
    last_name varchar(50), 
    token_id varchar(64),
    CONSTRAINT FOREIGN KEY (token_id) REFERENCES token(bearer) ON DELETE CASCADE
);

CREATE TABLE token (
    bearer varchar(64) PRIMARY KEY, 
    expiration_date DATE
);
