-- Create database
CREATE DATABASE IF NOT EXISTS sql_learning_platform;
USE sql_learning_platform;

-- User table
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    profile_info TEXT,
    last_login DATETIME,
    role ENUM('Student', 'Instructor', 'Admin') NOT NULL DEFAULT 'Student',
    INDEX idx_email (email),
    date_joined DATETIME NOT NULL
);
ALTER TABLE User
ADD COLUMN is_superuser BOOLEAN DEFAULT FALSE AFTER role,
ADD COLUMN is_staff BOOLEAN DEFAULT FALSE AFTER is_superuser,
ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER is_staff;

-- Student table
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    FOREIGN KEY (student_id) REFERENCES User(user_id) ON DELETE CASCADE 
);

-- Instructor table
CREATE TABLE Instructor (
    instructor_id INT PRIMARY KEY,
    department VARCHAR(100),
    FOREIGN KEY (instructor_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Admin table
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY,
    access_level VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    FOREIGN KEY (admin_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Topic table
CREATE TABLE Topic (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- SQLProblem table
CREATE TABLE SQLProblem (
    problem_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    difficulty_level ENUM('Easy', 'Medium', 'Hard', 'Expert') NOT NULL,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    topic_id INT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES Topic(topic_id) ON DELETE CASCADE,
    INDEX idx_topic (topic_id),
    INDEX idx_difficulty (difficulty_level)
);

-- Hint table
CREATE TABLE Hint (
    hint_id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT NOT NULL,                 
    hint_text TEXT NOT NULL,                 
    hint_order INT DEFAULT 1,                 
    FOREIGN KEY (problem_id) REFERENCES SQLProblem(problem_id) ON DELETE CASCADE,
    INDEX idx_problem (problem_id)
);

-- Attempt table
CREATE TABLE Attempt (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    problem_id INT NOT NULL,
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    score DECIMAL(5,2) DEFAULT 0,
    time_taken INT COMMENT 'Time taken in seconds',
    status ENUM('Completed', 'In Progress', 'Failed', 'Abandoned') NOT NULL,
    hints_used INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES SQLProblem(problem_id) ON DELETE CASCADE,
    INDEX idx_user_problem (user_id, problem_id)
);

-- Message table
CREATE TABLE Message (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message_content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE, 
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES User(user_id) ON DELETE CASCADE,
    INDEX idx_sender (sender_id),
    INDEX idx_receiver (recetoken_idiver_id)
);

-- Notification table
CREATE TABLE Notification (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    comment_message BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (receiver_id) REFERENCES User(user_id) ON DELETE CASCADE,
    INDEX idx_receiver (receiver_id)
);

-- Comment table
CREATE TABLE Comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (problem_id) REFERENCES SQLProblem(problem_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    INDEX idx_problem (problem_id),
    INDEX idx_user (user_id)
);

-- LearningAnalytics table
CREATE TABLE LearningAnalytics (
    analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    problem_id INT NOT NULL,
    error_frequency INT DEFAULT 0,
    time_spent INT DEFAULT 0 COMMENT 'Time spent in seconds',
    completion_status ENUM('Completed', 'In Progress', 'Abandoned') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES SQLProblem(problem_id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_problem (problem_id)
);

-- Badge table
CREATE TABLE Badge (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    criteria TEXT NOT NULL,
    icon VARCHAR(255)
);

-- StudentBadge table (for many-to-many relationship)
CREATE TABLE StudentBadge (
    student_id INT NOT NULL,
    badge_id INT NOT NULL,
    earned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, badge_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES Badge(badge_id) ON DELETE CASCADE
    
);



-- Create a user index table for tracking user count
CREATE TABLE UserIndex (
    current_index INT NOT NULL DEFAULT 0
);

-- Initialize the user index
INSERT INTO UserIndex (current_index) VALUES (0);

-- Trigger to increase user index when a new user is added
DELIMITER //
CREATE TRIGGER after_user_insert
AFTER INSERT ON User
FOR EACH ROW
BEGIN
    UPDATE UserIndex SET current_index = current_index + 1;
END//
DELIMITER ;

-- Trigger that automatically inserts a norification when a message is received from sender
DELIMITER //

CREATE TRIGGER after_message_insert
AFTER INSERT ON Message
FOR EACH ROW
BEGIN
    INSERT INTO Notification (receiver_id, content, is_read, timestamp, comment_message)
    VALUES (NEW.receiver_id, CONCAT('New message from ', (SELECT name FROM User WHERE user_id = NEW.sender_id)), FALSE, NOW(), FALSE);
END;
//

DELIMITER ;

-- Trigger that automatically assign users to different roles (Students, Instructors, Admins)
DELIMITER //
CREATE TRIGGER after_user_insert_role
AFTER INSERT ON User
FOR EACH ROW
BEGIN
    IF NEW.role = 'Student' THEN
        INSERT INTO Student (student_id) VALUES (NEW.user_id);
    ELSEIF NEW.role = 'Instructor' THEN
        INSERT INTO Instructor (instructor_id, department) VALUES (NEW.user_id, 'Unknown');
    ELSEIF NEW.role = 'Admin' THEN
         INSERT INTO Admin (admin_id, access_level, department) VALUES (NEW.user_id, 'Standard', 'Unknown');
    END IF;
END;
//
DELIMITER ;

-- Function to calculate student progress on a topic
DELIMITER //
CREATE FUNCTION CalculateTopicProgress(
    p_student_id INT,
    p_topic_id INT
) RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE total_problems INT;
    DECLARE solved_problems INT;
    DECLARE progress_percentage FLOAT;
    
    -- Count total problems in the topic
    SELECT COUNT(*) INTO total_problems
    FROM SQLProblem
    WHERE topic_id = p_topic_id;
    
    -- Count solved problems by the student
    SELECT COUNT(DISTINCT A.problem_id) INTO solved_problems
    FROM Attempt A
    JOIN SQLProblem P ON A.problem_id = P.problem_id
    WHERE A.student_id = p_student_id
    AND P.topic_id = p_topic_id
    AND A.status = 'Completed'
    AND A.score >= 70; -- Assuming 70% is passing
    
    -- Calculate progress percentage
    IF total_problems > 0 THEN
        SET progress_percentage = (solved_problems / CAST(total_problems AS FLOAT)) * 100;
    ELSE
        SET progress_percentage = 0;
    END IF;
    
    RETURN progress_percentage;
END//
DELIMITER ;

-- Stored procedure to assign badges based on criteria
DELIMITER //
CREATE PROCEDURE AssignBadges(IN p_student_id INT)
BEGIN
    -- SQL Master badge (Completed at least 50 SQL problems)
    IF (SELECT COUNT(*) FROM Attempt WHERE student_id = p_student_id AND status = 'Completed' AND score >= 80) >= 50 THEN
        IF NOT EXISTS (SELECT 1 FROM StudentBadge WHERE student_id = p_student_id AND badge_id = (SELECT badge_id FROM Badge WHERE name = 'SQL Master')) THEN
            INSERT IGNORE INTO StudentBadge (student_id, badge_id)
            SELECT p_student_id, badge_id FROM Badge WHERE name = 'SQL Master';
        END IF;
    END IF;
    
    -- Quick Solver badge (Solved at least 10 problems in less than 5 minutes each)
    IF (SELECT COUNT(*) FROM Attempt WHERE student_id = p_student_id AND status = 'Completed' AND time_taken < 300) >= 10 THEN
        IF NOT EXISTS (SELECT 1 FROM StudentBadge WHERE student_id = p_student_id AND badge_id = (SELECT badge_id FROM Badge WHERE name = 'Quick Solver')) THEN
            INSERT IGNORE INTO StudentBadge (student_id, badge_id)
            SELECT p_student_id, badge_id FROM Badge WHERE name = 'Quick Solver';
        END IF;
    END IF;
    
    -- Persistence badge (Attempted a problem at least 5 times before succeeding)
    IF EXISTS (
        SELECT problem_id, COUNT(*) as attempts
        FROM Attempt
        WHERE student_id = p_student_id
        GROUP BY problem_id
        HAVING COUNT(*) >= 5
        LIMIT 1
    ) THEN
        IF NOT EXISTS (SELECT 1 FROM StudentBadge WHERE student_id = p_student_id AND badge_id = (SELECT badge_id FROM Badge WHERE name = 'Persistence')) THEN
            INSERT IGNORE INTO StudentBadge (student_id, badge_id)
            SELECT p_student_id, badge_id FROM Badge WHERE name = 'Persistence';
        END IF;
    END IF;
END//
DELIMITER ;

-- Create a view for student performance analytics
-- CREATE VIEW StudentPerformanceView AS
-- SELECT 
--     S.student_id,
--     U.name AS student_name,
--     T.topic_id,
--     T.name AS topic_name,
--     COUNT(DISTINCT A.problem_id) AS problems_attempted,
--     SUM(CASE WHEN A.status = 'Completed' THEN 1 ELSE 0 END) / NULLIF(COUNT(A.attempt_id), 0) * 100 AS completion_rate,
--     AVG(A.score) AS average_score,
--     AVG(A.time_taken) AS average_time_taken,
--     AVG(A.hints_used) AS average_hints_used
-- FROM 
--     Student S
--     JOIN User U ON S.student_id = U.user_id
--     JOIN Attempt A ON S.student_id = A.student_id
--     JOIN SQLProblem P ON A.problem_id = P.problem_id
--     JOIN Topic T ON P.topic_id = T.topic_id
-- GROUP BY 
--     S.student_id, T.topic_id;

-- Create a view for problem difficulty statistics
CREATE VIEW ProblemDifficultyStats AS
SELECT 
    P.problem_id,
    P.title,
    P.difficulty_level,
    T.name AS topic_name,
    COUNT(A.attempt_id) AS total_attempts,
    AVG(A.score) AS average_score,
    AVG(A.time_taken) AS average_time_taken,
    SUM(CASE WHEN A.status = 'Completed' THEN 1 ELSE 0 END) / COUNT(A.attempt_id) * 100 AS completion_rate
FROM 
    SQLProblem P
    LEFT JOIN Attempt A ON P.problem_id = A.problem_id
    JOIN Topic T ON P.topic_id = T.topic_id
GROUP BY 
    P.problem_id;