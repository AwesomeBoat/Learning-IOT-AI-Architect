-- Database: test

-- DROP DATABASE IF EXISTS test;

CREATE TABLE T_office(
office_id INTEGER,
office_adress VARCHAR(30),
CONSTRAINT PK_office PRIMARY KEY (office_id)
);

CREATE TABLE T_course(
crs_code CHAR(8) NOT NULL PRIMARY KEY,
crs_name VARCHAR(30),
CONSTRAINT UK_crs UNIQUE (crs_name)
);

CREATE TABLE T_professor(
prf_id INTEGER NOT NULL PRIMARY KEY,
prf_name VARCHAR(30),
prf_course CHAR(8)
CONSTRAINT PK_course REFERENCES T_course (crs_code)
ON DELETE SET NULL,
office_id INTEGER REFERENCES T_office,
CONSTRAINT prf_name UNIQUE (prf_name)
);