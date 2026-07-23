SELECT last_name, login, year_result
FROM student
WHERE LEFT(last_name, 1) IN ('D','M','S')
ORDER BY birth_date 