-- Exo 2.7.1
SELECT last_name, first_name, section_id
FROM student
WHERE section_id = (SELECT section_id FROM student WHERE last_name = 'Roberts')
AND last_name != 'Roberts'
ORDER BY last_name;

-- Exo 2.7.2
SELECT last_name, first_name, year_result
FROM student
WHERE year_result > 2*(SELECT AVG(year_result) FROM student);

-- Exo 2.7.3
SELECT section_id, section_name
FROM section
WHERE section_id NOT IN (SELECT section_id FROM professor);

-- Exo 2.7.4
SELECT last_name, first_name, TO_CHAR(birth_date, 'DD/MM/YYYY') 
AS "Date de naissance", year_result
FROM student
WHERE TO_CHAR(birth_date,'MM') = (SELECT TO_CHAR(professor_hire_date,'MM') FROM professor WHERE professor_name = 'giot');

-- Exo 2.7.5
SELECT last_name, first_name, year_result
FROM student
WHERE year_result BETWEEN 
(SELECT lower_bound FROM grade AS g WHERE g.grade = 'TB')
AND
(SELECT upper_bound FROM grade g WHERE g.grade='TB');

-- Exo 2.7.6

SELECT last_name, first_name, section_id
FROM student
WHERE section_id = (SELECT section_id FROM professor WHERE professor_surname = 'Marceau');


SELECT s.last_name, s.first_name, s.section_id
FROM student AS s, section AS sec
WHERE s.section_id = (SELECT section_id FROM section WHERE last_name = "Marceau")


