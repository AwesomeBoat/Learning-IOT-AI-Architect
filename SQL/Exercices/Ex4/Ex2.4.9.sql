SELECT TO_CHAR(birth_date, 'MM')::INTEGER AS "Mois de naissance", AVG(year_result)::INTEGER
FROM student
WHERE TO_CHAR(birth_date,'YYYY')::INTEGER BETWEEN 1970 AND 1985
GROUP BY "Mois de naissance"