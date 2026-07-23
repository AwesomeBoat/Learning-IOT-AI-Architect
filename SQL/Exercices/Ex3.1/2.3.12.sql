SELECT login, TO_CHAR(birth_date, 'YYYY')
FROM student
WHERE TO_CHAR(birth_date, 'YYYY') > '1970'