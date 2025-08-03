#!/bin/bash
# HBnB Database Test Runner

echo "HBnB Database Test Suite"
echo "========================"

# Test 1: Verify password hash
echo "1. Testing password hash verification..."
python3 verify_password.py

# Test 2: Generate new hashes
echo "2. Testing hash generation..."
python3 generate_hash.py > /dev/null 2>&1

echo "Test Suite Complete!"
