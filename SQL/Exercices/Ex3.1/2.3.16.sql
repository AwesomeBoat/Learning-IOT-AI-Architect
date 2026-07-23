SELECT first_name last_name, login, CONCAT(RIGHT(first_name, 3), (TO_CHAR(NOW(), 'YYYY')::INTEGER -TO_CHAR(birth_date, 'YYYY')::INTEGER)) AS "Nouveau login"
FROM student
WHERE year_result IN ('10','12','14')