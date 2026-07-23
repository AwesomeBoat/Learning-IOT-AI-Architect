SELECT section_id, AVG(year_result) AS "Moyenne", MAX(year_result) AS "Résultat maximum"
FROM student
GROUP BY section_id
HAVING AVG(year_result) >8