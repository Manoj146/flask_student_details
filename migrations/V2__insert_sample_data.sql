INSERT INTO students (name, email) VALUES ('Alice', 'alice@mail.com'), ('Bob', 'bob@mail.com');
INSERT INTO subjects (name) VALUES ('Math'), ('Science');
INSERT INTO teachers (username, password) VALUES ('teacher1', '$pbkdf2-sha256$...'); -- hash of "password"
INSERT INTO grades (student_id, subject_id, score) VALUES (1, 1, 85), (2, 2, 90);
