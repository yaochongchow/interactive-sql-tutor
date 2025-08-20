-- Insert data into User table
INSERT INTO User (name, email, password, profile_info, last_login, role, date_joined) VALUES
('Alice Johnson', 'alice@email.com', 'hashed_password_1', 'Passionate about SQL.', '2024-03-10 12:30:00', 'Student', '2024-02-01'),
('Bob Smith', 'bob@email.com', 'hashed_password_2', 'Expert in database management.', '2024-03-11 15:20:00', 'Instructor', '2024-01-15'),
('Charlie Brown', 'charlie@email.com', 'hashed_password_3', 'Backend developer specializing in SQL optimization.', '2024-03-12 09:15:00', 'Instructor', '2023-12-20'),
('David Miller', 'david@email.com', 'hashed_password_4', 'System administrator for SQL platforms.', '2024-03-13 10:45:00', 'Admin', '2023-11-10'),
('Emma Watson', 'emma@email.com', 'hashed_password_5', 'Data analyst focusing on big data.', '2024-03-14 18:00:00', 'Student', '2024-02-05'),
('Frank Thomas', 'frank@email.com', 'hashed_password_6', 'Full-stack developer.', '2024-03-15 21:10:00', 'Student', '2024-02-10'),
('Grace Hopper', 'grace@email.com', 'hashed_password_7', 'Legendary computer scientist.', '2024-03-16 08:25:00', 'Admin', '2023-10-05'),
('Henry Ford', 'henry@email.com', 'hashed_password_8', 'Machine Learning Engineer.', '2024-03-17 14:40:00', 'Student', '2024-02-15'),
('Ivy Green', 'ivy@email.com', 'hashed_password_9', 'Data Science Researcher.', '2024-03-18 19:30:00', 'Student', '2024-02-20'),
('Jack Daniels', 'jack@email.com', 'hashed_password_10', 'Database Administrator.', '2024-03-19 11:20:00', 'Student', '2024-01-30'),
('Kate Winslet', 'kate@email.com', 'hashed_password_11', 'Software Engineer.', '2024-03-20 17:15:00', 'Student', '2023-12-10'),
('Luke Skywalker', 'luke@email.com', 'hashed_password_12', 'SQL Performance Expert.', '2024-03-21 10:05:00', 'Instructor', '2023-11-25'),
('Monica Bell', 'monica@email.com', 'hashed_password_13', 'Network Security Specialist.', '2024-03-22 09:45:00', 'Instructor', '2023-11-05'),
('Nathan Drake', 'nathan@email.com', 'hashed_password_14', 'System Architect.', '2024-03-23 13:55:00', 'Instructor', '2023-10-30'),
('Olivia Benson', 'olivia@email.com', 'hashed_password_15', 'Lead SQL Trainer.', '2024-03-24 18:25:00', 'Instructor', '2023-10-15'),
('Paul Newman', 'paul@email.com', 'hashed_password_16', 'Senior DBA.', '2024-03-25 14:10:00', 'Instructor', '2023-09-30'),
('Quincy Jones', 'quincy@email.com', 'hashed_password_17', 'Infrastructure Engineer.', '2024-03-26 12:45:00', 'Admin', '2023-09-15'),
('Rachel Adams', 'rachel@email.com', 'hashed_password_18', 'Data Governance Specialist.', '2024-03-27 16:40:00', 'Admin', '2023-09-01'),
('Steve Rogers', 'steve@email.com', 'hashed_password_19', 'Cloud Database Engineer.', '2024-03-28 11:35:00', 'Admin', '2023-08-20'),
('Tony Stark', 'tony@email.com', 'hashed_password_20', 'High-Performance Computing.', '2024-03-29 20:50:00', 'Admin', '2023-08-10'),
('Uma Thurman', 'uma@email.com', 'hashed_password_21', 'Enterprise Architect.', '2024-03-30 09:55:00', 'Admin', '2023-07-30');

-- Update Instructor departments
UPDATE Instructor SET department = 'Computer Science' WHERE instructor_id = 2;
UPDATE Instructor SET department = 'Information Technology' WHERE instructor_id = 3;
UPDATE Instructor SET department = 'Data Science' WHERE instructor_id = 12;
UPDATE Instructor SET department = 'Cybersecurity' WHERE instructor_id = 13;
UPDATE Instructor SET department = 'Cloud Computing' WHERE instructor_id = 14;
UPDATE Instructor SET department = 'Software Engineering' WHERE instructor_id = 15;
UPDATE Instructor SET department = 'Database Administration' WHERE instructor_id = 16;

-- Update Admin access levels and departments
UPDATE Admin SET access_level = 'SuperAdmin', department = 'System Administration' WHERE admin_id = 4;
UPDATE Admin SET access_level = 'Moderator', department = 'Platform Support' WHERE admin_id = 7;
UPDATE Admin SET access_level = 'Data Security', department = 'Data Management' WHERE admin_id = 17;
UPDATE Admin SET access_level = 'DBA', department = 'Database Maintenance' WHERE admin_id = 18;
UPDATE Admin SET access_level = 'Infrastructure Lead', department = 'Cloud Computing' WHERE admin_id = 19;
UPDATE Admin SET access_level = 'Compliance', department = 'Data Governance' WHERE admin_id = 20;
UPDATE Admin SET access_level = 'Network Admin', department = 'IT Operations' WHERE admin_id = 21;

-- Insert data into Topic table
INSERT INTO Topic (name, description) VALUES
('Select', 'Basic SELECT statements, filtering with WHERE, and projecting columns.'),
('Aggregation Functions', 'Using GROUP BY with functions like SUM, AVG, COUNT, MIN, and MAX.'),
('Sub Query', 'Using subqueries in SELECT, FROM, and WHERE clauses.'),
('Join', 'Understanding INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN.'),
('With', 'Using WITH clauses (Common Table Expressions) to simplify complex queries.'),
('In-Line View', 'Creating temporary views within queries for filtering and aggregation.'),
('Window Function', 'Advanced analytics using ROW_NUMBER(), RANK(), DENSE_RANK(), and PARTITION BY.');

-- Insert data into SQLProblem table
INSERT INTO SQLProblem (title, description, difficulty_level, topic_id) VALUES
('Find Active Users', 'Write an SQL query to find users who logged in within the last 7 days.', 'Easy', 1),
('Top Selling Products', 'Get the top 3 best-selling products from the sales table.', 'Medium', 2),
('Optimize Queries', 'Identify and optimize slow SQL queries in logs.', 'Hard', 3),
('Stored Procedure Task', 'Write a stored procedure to insert new employees.', 'Expert', 4),
('Find Orders with Subqueries', 'Use a subquery to find customers with the most orders.', 'Medium', 5),
('Ranking Employees', 'Use RANK() function to rank employees by salary.', 'Hard', 6),
('Database Normalization', 'Identify normalization issues in a given schema.', 'Expert', 7);

-- Insert data into Badge table
INSERT INTO Badge (name, criteria, icon) VALUES
('SQL Beginner', 'Complete 3 easy SQL problems.', 'beginner.png'),
('SQL Master', 'Solve all hard SQL problems.', 'master.png'),
('Performance Guru', 'Optimize at least 5 queries.', 'guru.png'),
('Stored Procedure Pro', 'Successfully create 3 stored procedures.', 'procedure.png'),
('Subquery Expert', 'Solve 5 problems using subqueries.', 'subquery.png'),
('Ranking Champion', 'Use ranking functions in at least 3 queries.', 'ranking.png'),
('Database Designer', 'Understand normalization and design a schema.', 'design.png');

-- Insert data into Attempt table
INSERT INTO Attempt (user_id, problem_id, submission_date, score, time_taken, status, hints_used) VALUES
(1, 1, '2024-03-10 14:00:00', 85.50, 120, 'Completed', 1),
(5, 2, '2024-03-11 16:30:00', 92.00, 150, 'Completed', 2),
(6, 3, '2024-03-12 10:15:00', 45.75, 200, 'Failed', 0),
(1, 4, '2024-03-13 18:45:00', 80.00, 300, 'Completed', 0),
(1, 5, '2024-03-14 18:45:00', 80.00, 300, 'Completed', 1),
(5, 6, '2025-03-15 18:45:00', 80.00, 300, 'Completed', 0),
(6, 6, '2025-03-15 18:45:00', 80.00, 300, 'Failed', 0),
(6, 7, '2025-03-16 18:45:00', 80.00, 300, 'Completed', 0);

-- Insert data into LearningAnalytics table
INSERT INTO LearningAnalytics (student_id, problem_id, error_frequency, time_spent, completion_status) VALUES
(1, 1, 2, 120, 'Completed'), 
(5, 2, 0, 150, 'Completed'), 
(6, 3, 5, 200, 'Abandoned'),
(8, 4, 1, 180, 'Completed'), 
(9, 5, 3, 170, 'In Progress'), 
(10, 6, 2, 190, 'Abandoned'),
(11, 7, 0, 220, 'Completed');

-- Insert data into StudentBadge table
INSERT INTO StudentBadge (student_id, badge_id, earned_date) VALUES
(1, 1, '2024-03-10 17:00:00'), 
(5, 2, '2024-03-11 19:00:00'), 
(6, 3, '2024-03-12 12:30:00'),
(8, 1, '2024-03-14 14:00:00'), 
(9, 2, '2024-03-15 10:30:00'), 
(10, 3, '2024-03-16 08:20:00'), 
(11, 1, '2024-03-17 16:40:00');

-- Insert data into Message table
INSERT INTO Message (sender_id, receiver_id, message_content, is_read, timestamp) VALUES
(2, 1, 'Please review the SQL joins lesson.', FALSE, '2024-03-10 14:30:00'),
(3, 5, 'Great job on the database optimization task!', TRUE, '2024-03-12 17:45:00'),
(4, 6, 'Your SQL problem submission has been reviewed.', FALSE, '2024-03-14 09:15:00'),
(1, 2, 'Can you explain subqueries in more detail?', FALSE, '2024-03-15 13:50:00'),
(3, 5, 'I am struggling with ranking employees using RANK().', TRUE, '2024-03-16 19:00:00'),
(6, 4, 'I found a better way to optimize the query!', FALSE, '2024-03-17 08:40:00'),
(7, 1, 'Here is a resource on database normalization.', TRUE, '2024-03-18 10:30:00');

-- Insert data into Comment table
INSERT INTO Comment (problem_id, user_id, content, timestamp) VALUES
(1, 1, 'This problem was really helpful!', '2024-03-10 16:00:00'),
(2, 5, 'I found the GROUP BY concept a bit tricky.', '2024-03-12 20:15:00'),
(3, 6, 'Indexes made my queries much faster!', '2024-03-14 11:30:00'),
(4, 5, 'Stored procedures are very useful for automation.', '2024-03-15 14:45:00'),
(5, 6, 'Subqueries can be confusing at first, but they are powerful.', '2024-03-16 09:20:00'),
(6, 1, 'The RANK() function is great for handling ties in rankings.', '2024-03-17 10:10:00'),
(7, 5, 'I never realized how important normalization is.', '2024-03-18 12:00:00');

-- Insert data into Notification table
INSERT INTO Notification (receiver_id, content, is_read, timestamp, comment_message) VALUES
(1, 'New SQL challenge available!', FALSE, '2024-03-10 10:00:00', FALSE),
(5, 'Your attempt on the SQL problem has been graded.', TRUE, '2024-03-11 18:45:00', TRUE),
(6, 'Reminder: Complete the database indexing lesson.', FALSE, '2024-03-13 08:00:00', FALSE),
(3, 'A new discussion has started in the forum.', FALSE, '2024-03-14 11:30:00', TRUE),
(2, 'Your comment received a reply!', TRUE, '2024-03-15 15:20:00', TRUE),
(5, 'Your ranking has improved on the leaderboard!', FALSE, '2024-03-16 09:45:00', FALSE),
(1, 'You earned a new badge: SQL Master!', TRUE, '2024-03-17 14:10:00', TRUE);