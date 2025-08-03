-- Test Database Constraints
-- Test unique email constraint
INSERT INTO users (id, first_name, last_name, email, password)
VALUES (
        'test-user-unique',
        'Test',
        'User',
        'admin@hbnb.io',
        'password123'
    );
-- Test rating constraint
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
        'test-review-bad',
        'Bad rating',
        6,
        'test-user',
        'test-place'
    );
SELECT 'Constraint tests completed' as result;
