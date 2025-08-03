-- Complete HBnB Database Setup Script

-- Source the table creation script
SOURCE create_tables.sql;

-- Source the initial data insertion script
SOURCE insert_initial_data.sql;

-- Display setup completion message
SELECT 'Database setup completed successfully!' as status;
