# HBnB Database SQL Scripts

This directory contains production SQL scripts for creating and managing the HBnB database schema.

## Production Files

- `create_tables.sql` - Creates all database tables with relationships and constraints
- `insert_initial_data.sql` - Inserts admin user and initial amenities
- `setup_database.sql` - Complete database setup (runs both scripts above)

## Usage

```sql
-- Complete database setup (recommended)
mysql -u username -p database_name < setup_database.sql

-- Or run individually
mysql -u username -p database_name < create_tables.sql
mysql -u username -p database_name < insert_initial_data.sql
```

## Database Schema

### Tables Created:

- **users** - User accounts with bcrypt password hashing
- **places** - Rental properties with owner relationships
- **reviews** - User reviews with rating constraints (1-5)
- **amenities** - Available amenities for places
- **place_amenity** - Many-to-many relationship table

### Initial Data:

- Admin user: admin@hbnb.io (password: admin1234)
- Three amenities: WiFi, Swimming Pool, Air Conditioning

## Testing

All database tests have been moved to the `../tests/sql/` directory.
See `../tests/README.md` for testing instructions.
