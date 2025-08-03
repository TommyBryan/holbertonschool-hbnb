-- HBnB Database Initial Data Insertion Script

-- Insert Administrator User
INSERT INTO users (
    id, 
    first_name, 
    last_name, 
    email, 
    password, 
    is_admin, 
    created_at, 
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$UmzJqflj1LycGiHMV7ZA9.ehb5nqPMD.0jgMV1kziMzJl0aVe2qG.',
    TRUE,
    NOW(),
    NOW()
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
    ('0ce36968-014b-4ef1-b1e1-be02ecec2cc8', 'WiFi', NOW(), NOW()),
    ('0a1b0c78-4a47-454c-99f5-1e043f1600ae', 'Swimming Pool', NOW(), NOW()),
    ('2f2414dd-05fc-4b9c-88eb-bd926e8ede30', 'Air Conditioning', NOW(), NOW());

-- Verify the insertions
SELECT 'Users inserted:' as info;
SELECT id, first_name, last_name, email, is_admin FROM users;

SELECT 'Amenities inserted:' as info;
SELECT id, name FROM amenities;
