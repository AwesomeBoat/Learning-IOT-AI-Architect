-- Select O.*, D.quantity, D.product_id, P.product_name
-- FROM orders AS O
-- JOIN order_details AS D ON D.order_id = O.order_id
-- JOIN products AS P ON P.product_id = D.product_id;


-- CREATE TABLE IF NOT EXISTS student(
-- 	nom TEXT,
-- 	ref_voiture INT
-- );

-- CREATE TABLE IF NOT EXISTS voiture(
-- 	numero INT,
-- 	marque TEXT
-- );


-- INSERT INTO student (nom, ref_voiture) VALUES('Benoit',1);
-- INSERT INTO student  VALUES('Jean',2);
-- INSERT INTO student VALUES ('Tanguy');

-- SELECT * FROM student;

-- INSERT INTO voiture VALUES(1, 'Skoda'), (2,'Ferrari'), (3,'BMW');

-- SELECT * FROM student;
-- SELECT * FROM voiture;

-- SELECT *
-- FROM student AS S
-- LEFT JOIN voiture AS V ON V.numero = S.ref_voiture

-- SELECT * 
-- FROM student AS S

-- CROSS JOIN voiture AS V;


-- SELECT * 
-- FROM student AS S

-- JOIN products AS P ON P.product_id = S.ref_voiture;


