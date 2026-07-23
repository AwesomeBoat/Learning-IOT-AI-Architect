SELECT section_id, AVG(year_result) AS "Moyenne"
FROM student
GROUP BY section_id
HAVING COUNT(section_id) >3
ORDER BY section_id