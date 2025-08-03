#!/usr/bin/env python3
import bcrypt
import uuid

def generate_password_hash(password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

def generate_uuid():
    return str(uuid.uuid4())

if __name__ == "__main__":
    admin_password = "admin1234"
    admin_hash = generate_password_hash(admin_password)
    
    wifi_id = generate_uuid()
    pool_id = generate_uuid()
    ac_id = generate_uuid()
    
    print("Generated values for SQL insert:")
    print("=" * 50)
    print(f"Admin password hash: {admin_hash}")
    print(f"WiFi amenity ID: {wifi_id}")
    print(f"Swimming Pool amenity ID: {pool_id}")
    print(f"Air Conditioning amenity ID: {ac_id}")
    print("=" * 50)
