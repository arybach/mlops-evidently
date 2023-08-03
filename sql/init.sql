-- Create a new user with the desired username and password
CREATE USER '${DB_USER}' WITH PASSWORD '${DB_USER_PASSWORD}';

-- Grant all privileges on the monitoring_db database to the new user
GRANT ALL PRIVILEGES ON DATABASE monitoring_db TO '${DB_USER}';
