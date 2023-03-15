# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 09:28:56 2023

@author: Olivier
"""

CREATE DATABASE testdb;
USE testdb;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users (name, email) VALUES
  ('John Doe', 'johndoe@example.com'),
  ('Jane Doe', 'janedoe@example.com'),
  ('Bob Smith', 'bobsmith@example.com');

GRANT ALL PRIVILEGES ON testdb.* TO 'user'@'%' IDENTIFIED BY 'user-password' WITH GRANT OPTION;
FLUSH PRIVILEGES;