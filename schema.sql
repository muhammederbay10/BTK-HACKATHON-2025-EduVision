-- Create USERS table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
);

-- Create REPORTS table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    date_time TIMESTAMP NOT NULL,
    lesson_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create REPORT_CONTENT table
CREATE TABLE report_content (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);

-- Create STUDENT_PROFESSION table
CREATE TABLE student_profession (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL,
    average VARCHAR(10),
    image VARCHAR(500),
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_date_time ON reports(date_time);
CREATE INDEX idx_report_content_report_id ON report_content(report_id);
CREATE INDEX idx_student_profession_report_id ON student_profession(report_id);

-- Optional: Add some constraints
ALTER TABLE users ADD CONSTRAINT chk_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
ALTER TABLE reports ADD CONSTRAINT chk_status_values CHECK (status IN ('pending', 'processing', 'completed', 'failed'));