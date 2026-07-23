SELECT last_name, year_result,
CASE
	WHEN year_result < 10 THEN 'Inférieure'
	WHEN year_result = 10 THEN 'Neutre'
	ELSE 'Supérieur'
END AS "Catégorie"
FROM student
WHERE TO_CHAR(birth_date, 'YYYY')::INTEGER BETWEEN 1955 AND 1965