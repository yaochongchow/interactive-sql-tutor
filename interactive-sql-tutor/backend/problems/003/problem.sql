Drop table IF EXISTS Students;
Create table Students (
student_id int, 
student_name  varchar(30), 
major varchar(100));
insert into Students (student_id, student_name, major) values ('1', 'Daniel', 'MSCS');
insert into Students (student_id, student_name, major) values ('2', 'Alice', '');
insert into Students (student_id, student_name, major) values ('3', 'Bob', 'BSCS');
insert into Students (student_id, student_name, major) values ('4', 'George', 'MSEE-CE');
insert into Students (student_id, student_name, major) values ('5', 'Alain', 'MSCS');