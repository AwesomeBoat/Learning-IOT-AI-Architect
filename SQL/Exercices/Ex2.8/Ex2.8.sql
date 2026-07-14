SELECT CONCAT(last_name, ' ', first_name),
	year_result
FROM student
WHERE section_id LIKE '1010'
ORDER BY last_name ASC