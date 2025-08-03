#!/usr/bin/env python3
import bcrypt

# Test the generated hash
stored_hash = "$2b$12$UmzJqflj1LycGiHMV7ZA9.ehb5nqPMD.0jgMV1kziMzJl0aVe2qG."
test_password = "admin1234"

# Verify the password
is_valid = bcrypt.checkpw(test_password.encode('utf-8'), stored_hash.encode('utf-8'))

print(f"Password verification test:")
print(f"Password: {test_password}")
print(f"Hash: {stored_hash}")
print(f"Valid: {is_valid}")

if is_valid:
    print("Password hash is correct!")
else:
    print("Password hash verification failed!")
