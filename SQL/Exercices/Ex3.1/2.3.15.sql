SELECT first_name, last_name, login, CONCAT(SUBSTRING(first_name FROM 1 FOR 2), SUBSTRING(last_name FROM 1 FOR 4)) AS "New login"
FROM student
WHERE year_result BETWEEN 6 AND 10