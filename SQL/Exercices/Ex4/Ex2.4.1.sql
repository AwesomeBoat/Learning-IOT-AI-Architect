

SELECT section_id, AVG(year_result)
FROM student
WHERE year_result > 10
GROUP BY section_id;