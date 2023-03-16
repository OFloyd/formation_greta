from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

# create the FastAPI instance
app = FastAPI()

# create the database engine
engine = create_engine("mysql://root:pass@localhost:3306/employees")

# reflect the database schema to an ORM base
Base = automap_base()
Base.prepare(engine, reflect=True)

# map the tables to ORM classes
Employees = Base.classes.employees
Departments = Base.classes.departments
Dept_Emp = Base.classes.dept_emp
Salaries = Base.classes.salaries

# create a function to get a database session
def get_db():
    try:
        db = Session(bind=engine)
        yield db
    finally:
        db.close()
