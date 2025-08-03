# HBnB Database Tests

This directory contains all database tests for the HBnB project.

## Files:

- test_crud.sql - CRUD operations testing
- test_constraints.sql - Constraint validation
- test_performance.sql - Performance testing
- verify_password.py - Password hash verification
- generate_hash.py - Hash/UUID generation
- run_tests.sh - Test runner script

## Usage:

```bash
./run_tests.sh  # Run all tests
mysql -u user -p db < test_crud.sql  # Individual test
```
