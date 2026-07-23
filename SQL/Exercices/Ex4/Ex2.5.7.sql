SELECT course_id, section_id, AVG(year_result) AS "Moyenne"
FROM student
WHERE section_id IN ('1010','1320')
GROUP BY CUBE (course_id, section_id)
ORDER BY (course_id, section_id)