SELECT last_name, year_result, TO_CHAR(birth_date, 'FMDD TMmonth YYYY')
FROM student
WHERE TO_CHAR(birth_date, 'YYYY')::INTEGER BETWEEN 1975 AND 1985