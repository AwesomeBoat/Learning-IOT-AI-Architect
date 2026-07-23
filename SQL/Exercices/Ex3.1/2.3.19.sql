SELECT COUNT(last_name) AS "Nbre de nom de plus de 7 lettres"
FROM student
WHERE CHAR_LENGTH(last_name) > 7