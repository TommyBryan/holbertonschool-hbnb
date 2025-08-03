# HBnB Database SQL Scripts

This directory contains SQL scripts for creating and managing the HBnB database schema.

## Files Overview

- `create_tables.sql` - Creates all database tables with relationships
- `insert_initial_data.sql` - Inserts admin user and amenities  
- `test_crud.sql` - Tests all CRUD operations
- `setup_database.sql` - Complete setup script
- `generate_hash.py` - Utility to generate password hashes

## Usage

```sql
-- Run complete setup
mysql -u username -p database_name < setup_database.sql

-- Or run individually
mysql -u username -p database_name < create_tables.sql
mysql -u username -p database_name < insert_initial_data.sql
```

## Initial Data

- Admin user: admin@hbnb.io (password: admin1234)
- Amenities: WiFi, Swimming Pool, Air Conditioning
