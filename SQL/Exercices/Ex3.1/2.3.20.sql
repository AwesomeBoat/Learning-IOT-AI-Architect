SELECT last_name, year_result,
CASE 
	WHEN year_result >= 12 THEN 'OK'
	ELSE 'KO'
END AS "Statut"
FROM student
WHERE TO_CHAR(birth_date, 'YYYY')::INTEGER < 1955