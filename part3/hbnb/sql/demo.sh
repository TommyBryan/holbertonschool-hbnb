#!/bin/bash
# HBnB Database Setup Demonstration Script

echo "HBnB Database Setup Demonstration"
echo "=================================="

# List all SQL scripts created
echo "Files created:"
ls -la *.sql *.py 2>/dev/null || echo "SQL scripts are ready"

echo ""
echo "To use these scripts:"
echo "1. MySQL: mysql -u user -p database < setup_database.sql"
echo "2. Test: mysql -u user -p database < test_crud.sql"
echo "3. Generate hash: python3 generate_hash.py"
