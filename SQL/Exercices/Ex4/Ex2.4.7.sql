SELECT section_id, MAX(year_result) AS "Résultat maximum"
FROM student
GROUP BY section_id