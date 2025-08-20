Drop table IF EXISTS Emp;
Drop table IF EXISTS Dept;
Create table Emp (
emp_id int,
emp_name varchar(45), 
gender varchar(6), 
dept_id int);
Create table Dept (
dept_id int, 
dept_name varchar(255));
insert into Emp (emp_id, emp_name, gender, dept_id) values ('1', 'Jack', 'M', '1');
insert into Emp (emp_id, emp_name, gender, dept_id) values ('2', 'Jane', 'F', '1');
insert into Emp (emp_id, emp_name, gender, dept_id) values ('3', 'Mark', 'M', '2');
insert into Dept (dept_id, dept_name) values ('1', 'Engineering');
insert into Dept (dept_id, dept_name) values ('2', 'Science');
insert into Dept (dept_id, dept_name) values ('3', 'Law');