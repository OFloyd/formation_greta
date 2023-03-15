#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:24:21 2023

@author: stagiaire
"""

from sqlalchemy import create_engine, inspect

# create an engine to connect to the database
engine = create_engine('mysql://user:password@localhost:3306/employees')

# create an inspector to get metadata about the database
inspector = inspect(engine)

# get a list of all the table names in the database
table_names = inspector.get_table_names()

# iterate over the table, select employees table and perform a query
for table_name in table_names:
    if table_name == 'employees':
        columns = inspector.get_columns(table_name)
        print(f"Table: {table_name}")
        for column in columns:
            print(f"{column['name']}: {column['type']}")
        print("\n")
        employees = engine.execute("SELECT * FROM employees WHERE gender = 'M' LIMIT 10")
        for row in employees:
            print(row)
