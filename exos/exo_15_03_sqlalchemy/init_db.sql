CREATE DATABASE company;

USE company;

-- Create Employees table
CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(50),
    Phone VARCHAR(20),
    HireDate DATE,
    Salary DECIMAL(10,2),
    CommissionPct DECIMAL(4,2),
    ManagerID INT,
    DepartmentID INT,
    JobID INT,
    LocationID INT,
    CONSTRAINT fk_manager FOREIGN KEY (ManagerID) REFERENCES Employees(EmployeeID),
    CONSTRAINT fk_department FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    CONSTRAINT fk_job FOREIGN KEY (JobID) REFERENCES Jobs(JobID),
    CONSTRAINT fk_location FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);

-- Create Departments table
CREATE TABLE Departments (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(50),
    ManagerID INT,
    LocationID INT,
    CONSTRAINT fk_department_manager FOREIGN KEY (ManagerID) REFERENCES Employees(EmployeeID),
    CONSTRAINT fk_department_location FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);

-- Create Projects table
CREATE TABLE Projects (
    ProjectID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectName VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    Budget DECIMAL(15,2)
);

-- Create Department_Projects table
CREATE TABLE Department_Projects (
    DepartmentID INT,
    ProjectID INT,
    CONSTRAINT fk_department_project_department FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    CONSTRAINT fk_department_project_project FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

-- Create Employee_Projects table
CREATE TABLE Employee_Projects (
    EmployeeID INT,
    ProjectID INT,
    HoursWorked DECIMAL(8,2),
    CONSTRAINT fk_employee_project_employee FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    CONSTRAINT fk_employee_project_project FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

-- Create Jobs table
CREATE TABLE Jobs (
    JobID INT AUTO_INCREMENT PRIMARY KEY,
    JobTitle VARCHAR(50),
    MinSalary DECIMAL(10,2),
    MaxSalary DECIMAL(10,2)
);

-- Create Locations table
CREATE TABLE Locations (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    Address VARCHAR(50),
    City VARCHAR(50),
    StateProvince VARCHAR(50),
    Country VARCHAR(50),
    PostalCode VARCHAR(50)
);


-- Insert 10 employees
INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_id, salary, manager_id, department_id)
VALUES
  ('John', 'Doe', 'johndoe@example.com', '555-555-1234', '2022-01-01', 1, 50000, NULL, 1),
  ('Jane', 'Doe', 'janedoe@example.com', '555-555-5678', '2022-01-01', 2, 60000, 1, 1),
  ('Bob', 'Smith', 'bobsmith@example.com', '555-555-9012', '2022-02-01', 3, 75000, 2, 2),
  ('Alice', 'Johnson', 'alicejohnson@example.com', '555-555-3456', '2022-02-01', 4, 85000, 2, 2),
  ('Mark', 'Lee', 'marklee@example.com', '555-555-7890', '2022-03-01', 5, 95000, 2, 3),
  ('Emily', 'Chen', 'emilychen@example.com', '555-555-2345', '2022-03-01', 5, 80000, 2, 3),
  ('Sara', 'Kim', 'sarakim@example.com', '555-555-6789', '2022-04-01', 6, 70000, 3, 4),
  ('Michael', 'Wu', 'michaelwu@example.com', '555-555-0123', '2022-04-01', 7, 65000, 3, 4),
  ('David', 'Nguyen', 'davidnguyen@example.com', '555-555-4567', '2022-05-01', 8, 55000, 4, 5),
  ('Jennifer', 'Garcia', 'jennifergarcia@example.com', '555-555-8901', '2022-05-01', 9, 60000, 4, 5);

-- Insert 3 departments
INSERT INTO departments (name, manager_id, location_id)
VALUES
  ('Engineering', 1, 1),
  ('Marketing', 2, 2),
  ('Sales', 3, 3);

-- Insert 4 projects
INSERT INTO projects (name, start_date, end_date)
VALUES
  ('Project A', '2022-01-01', '2022-03-01'),
  ('Project B', '2022-02-01', '2022-05-01'),
  ('Project C', '2022-03-01', '2022-06-01'),
  ('Project D', '2022-04-01', '2022-07-01');

-- Insert 4 department_projects relationships
INSERT INTO department_projects (department_id, project_id)
VALUES
  (1, 1),
  (1, 2),
  (2, 3),
  (3, 4);

-- insert 10 rows into department_projects table
INSERT INTO department_projects (department_id, project_id) VALUES
  (1, 1),
  (1, 2),
  (2, 1),
  (2, 3),
  (3, 2),
  (3, 3),
  (4, 1),
  (4, 2),
  (5, 1),
  (5, 3);

-- insert 10 rows into jobs table
INSERT INTO jobs (title, min_salary, max_salary) VALUES
  ('Manager', 70000, 120000),
  ('Salesperson', 20000, 40000),
  ('Developer', 50000, 100000),
  ('Accountant', 35000, 60000),
  ('HR Manager', 45000, 80000),
  ('Marketing Specialist', 40000, 75000),
  ('Administrative Assistant', 25000, 35000),
  ('Designer', 45000, 80000),
  ('Writer', 30000, 50000),
  ('Engineer', 55000, 90000);

-- insert 10 rows into location table
INSERT INTO location (city, state, country) VALUES
  ('New York', 'NY', 'USA'),
  ('Los Angeles', 'CA', 'USA'),
  ('San Francisco', 'CA', 'USA'),
  ('Chicago', 'IL', 'USA'),
  ('Houston', 'TX', 'USA'),
  ('London', NULL, 'England'),
  ('Paris', NULL, 'France'),
  ('Berlin', NULL, 'Germany'),
  ('Sydney', NULL, 'Australia'),
  ('Tokyo', NULL, 'Japan');

-- Insert 10 rows into the employee_projects table
INSERT INTO employee_projects (employee_id, project_id, start_date, end_date)
VALUES (1, 1, '2021-01-01', '2021-06-30'),
       (1, 2, '2021-07-01', '2021-12-31'),
       (2, 1, '2021-01-01', '2021-06-30'),
       (2, 3, '2021-07-01', '2021-12-31'),
       (3, 2, '2021-01-01', '2021-06-30'),
       (3, 3, '2021-07-01', '2021-12-31'),
       (4, 2, '2021-01-01', '2021-06-30'),
       (4, 1, '2021-07-01', '2021-12-31'),
       (5, 3, '2021-01-01', '2021-06-30'),
       (5, 1, '2021-07-01', '2021-12-31');
