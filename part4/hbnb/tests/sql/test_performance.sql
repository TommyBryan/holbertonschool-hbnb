-- Performance Tests
EXPLAIN
SELECT *
FROM users
WHERE email = 'admin@hbnb.io';
SELECT 'Performance tests completed' as result;
