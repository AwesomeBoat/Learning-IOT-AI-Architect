SELECT  section_id, course_id, AVG(year_result) AS "Moyenne"
FROM student
WHERE section_id IN ('1010','1320')
GROUP BY ROLLUP (course_id, section_id) 
ORDER BY section_id, course_id