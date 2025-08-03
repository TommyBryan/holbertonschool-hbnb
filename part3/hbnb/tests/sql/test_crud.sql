-- HBnB Database CRUD Operations Test Script

-- Test 1: INSERT operations
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
    ('test-user-1', 'John', 'Doe', 'john.doe@test.com', 'hashed_password', FALSE);

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
    ('test-place-1', 'Cozy Apartment', 'A nice place to stay', 99.99, 40.7128, -74.0060, 'test-user-1');

INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
    ('test-review-1', 'Great place to stay!', 5, 'test-user-1', 'test-place-1');

INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('test-place-1', '0ce36968-014b-4ef1-b1e1-be02ecec2cc8'),
    ('test-place-1', '2f2414dd-05fc-4b9c-88eb-bd926e8ede30');

-- Test 2: SELECT operations
SELECT 'All Users:' as test;
SELECT id, first_name, last_name, email, is_admin FROM users;

SELECT 'All Places:' as test;
SELECT id, title, price, owner_id FROM places;

SELECT 'All Reviews:' as test;
SELECT id, text, rating, user_id, place_id FROM reviews;

SELECT 'All Amenities:' as test;
SELECT id, name FROM amenities;

SELECT 'Place-Amenity Relationships:' as test;
SELECT pa.place_id, p.title, pa.amenity_id, a.name 
FROM place_amenity pa
JOIN places p ON pa.place_id = p.id
JOIN amenities a ON pa.amenity_id = a.id;

-- Test 3: UPDATE operations
UPDATE users SET first_name = 'Jane' WHERE id = 'test-user-1';
UPDATE places SET price = 89.99 WHERE id = 'test-place-1';
UPDATE reviews SET rating = 4 WHERE id = 'test-review-1';

-- Verify updates
SELECT 'Updated User:' as test;
SELECT id, first_name, last_name FROM users WHERE id = 'test-user-1';

SELECT 'Updated Place:' as test;
SELECT id, title, price FROM places WHERE id = 'test-place-1';

SELECT 'Updated Review:' as test;
SELECT id, text, rating FROM reviews WHERE id = 'test-review-1';

-- Test 4: DELETE operations
-- Delete the review first (due to foreign key constraints)
DELETE FROM reviews WHERE id = 'test-review-1';

-- Delete place-amenity relationships
DELETE FROM place_amenity WHERE place_id = 'test-place-1';

-- Delete the place
DELETE FROM places WHERE id = 'test-place-1';

-- Delete the user
DELETE FROM users WHERE id = 'test-user-1';

-- Verify deletions
SELECT 'Remaining test data (should be empty):' as test;
SELECT COUNT(*) as test_users FROM users WHERE id = 'test-user-1';
SELECT COUNT(*) as test_places FROM places WHERE id = 'test-place-1';
SELECT COUNT(*) as test_reviews FROM reviews WHERE id = 'test-review-1';

-- Test constraint violations
SELECT 'Testing constraint violations:' as test;

-- Try to insert a review with invalid rating (should fail)
-- INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
--     ('bad-review', 'Bad rating', 6, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'test-place-1');

-- Try to insert duplicate email (should fail)
-- INSERT INTO users (id, first_name, last_name, email, password) VALUES
--     ('duplicate-user', 'Duplicate', 'User', 'admin@hbnb.io', 'password');

SELECT 'CRUD tests completed successfully!' as result;
