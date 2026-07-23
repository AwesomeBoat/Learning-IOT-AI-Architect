-- Exo 2.6.1

SELECT c.course_name,  s.section_name, p.professor_name
FROM course AS c JOIN professor AS p ON c.professor_id = p.professor_id 
JOIN section AS s ON s.section_id = p.section_id; 

-- Exo 2.6.2

SELECT s.section_id, s.section_name, stu.last_name
FROM section as s JOIN student AS stu ON s.delegate_id = stu.student_id
ORDER BY section_id DESC;


-- Exo 2.6.3
SELECT s.section_id, s.section_name, p.professor_name
FROM section AS s LEFT JOIN professor as p ON s.section_id = p.section_id
ORDER BY section_id DESC;

-- Exo 2.6.4
SELECT s.section_id, s.section_name, p.professor_name
FROM section AS s JOIN professor as p ON s.section_id = p.section_id
ORDER BY section_id DESC;

-- Exo 2.6.5
SELECT s.last_name, s.year_result, g.grade
FROM grade AS g JOIN student AS s ON s.year_result BETWEEN g.lower_bound AND g.upper_bound
WHERE s.year_result >= 12
ORDER BY grade;

-- Exo 2.6.6
SELECT p.professor_name, s.section_name, c.course_name, c.course_ects
FROM professor AS p LEFT JOIN section AS s ON p.section_id = s.section_id  LEFT JOIN course AS c ON p.professor_id = c.professor_id
;
-- Exo 2.6.7
SELECT p.professor_id, c.course_ects, SUM(c.course_ects) As "ECTS_TOT"
FROM professor as p FULL JOIN course AS c ON c.professor_id = p.professor_id
GROUP BY p.professor_id, c.course_ects
ORDER BY "ECTS_TOT" DESC;

-- Exo 2.6.8
SELECT p.professor_name, p.professor_surname, 'P' AS "categorie"
FROM professor AS p
WHERE LENGTH(p.professor_surname) > 8
UNION
SELECT first_name, last_name, 'S' AS "categorie"
FROM student
WHERE LENGTH(last_name) > 8;

-- Exo 2.6.9
SELECT s.section_id
FROM section AS s
LEFT JOIN professor AS p
       ON s.section_id = p.section_id
WHERE p.professor_id IS NULL;



