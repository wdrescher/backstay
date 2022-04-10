CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE token (
    bearer varchar(64) PRIMARY KEY, 
    expiration_date DATE
);

CREATE TABLE profile (
    profile_id int PRIMARY KEY,
    email varchar(100) UNIQUE NOT NULL, 
    password varchar(30) not NULL,
    phone_number varchar(10), 
    first_name varchar(50), 
    last_name varchar(50), 
    token_id varchar(64),
    CONSTRAINT FOREIGN KEY (token_id) REFERENCES token(bearer) ON DELETE CASCADE
);

DROP PROCEDURE create_user; 
DELIMITER //

CREATE PROCEDURE create_user(IN bearer_token varchar(64), IN email varchar(64), IN my_password varchar(100), IN first_name varchar(50), IN last_name varchar(50))
BEGIN 
    INSERT INTO token (bearer, expiration_date) VALUES (bearer_token, CURDATE());
    INSERT INTO profile (email, first_name, last_name, password, token_id) VALUES (email, first_name, last_name, my_password, bearer_token);
END //

DELIMITER ;