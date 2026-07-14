SELECT last_name, section_id, year_result
FROM student
WHERE section_id IN ('1010','1020') AND year_result NOT BETWEEN 12 AND 18
ORDER BY section_id 