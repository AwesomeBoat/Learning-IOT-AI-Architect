SELECT last_name, login, year_result
FROM student
WHERE (year_result%2) != 0 AND year_result > 10
ORDER BY year_result DESC