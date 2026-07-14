SELECT last_name, section_id, year_result*5 AS "RESULTAT SUR 100"
FROM student
WHERE section_id LIKE '13%' AND year_result*5 <= 60
ORDER BY "RESULTAT SUR 100" DESC