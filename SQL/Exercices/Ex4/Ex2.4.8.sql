SELECT section_id, AVG(year_result) 
FROM student
WHERE LEFT(section_id, 2) = '10'
GROUP BY section_id
