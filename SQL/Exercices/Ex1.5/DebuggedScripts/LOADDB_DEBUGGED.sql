DROP TABLE grade CASCADE;
DROP TABLE student CASCADE;
DROP TABLE course CASCADE;
DROP TABLE professor CASCADE;
DROP TABLE section CASCADE;


CREATE TABLE section (
  section_id int NOT NULL,
  section_name varchar(50),
  delegate_id int NOT NULL,
  CONSTRAINT PK_section PRIMARY KEY (section_id)
);

CREATE TABLE Professor (
  professor_id int NOT NULL ,
  professor_name varchar(30) NOT NULL,
  professor_surname varchar(30) NOT NULL,
  section_id int NOT NULL,
  professor_office varchar(20) NOT NULL,
  professor_email varchar(30) NOT NULL,
  professor_hire_date timestamp NOT NULL,
  professor_wage int NOT NULL,
  CONSTRAINT PK_professor PRIMARY KEY (professor_id),
  constraint FK_professor_section foreign key (section_id) references section (section_id)
);






CREATE TABLE Course (
  course_id varchar(8) NOT NULL ,
  course_name varchar(200) NOT NULL ,
  course_ects decimal(3,1) NOT NULL,
  professor_id int,
  CONSTRAINT PK_course PRIMARY KEY (course_id),
  CONSTRAINT FK_course_professor FOREIGN KEY (professor_id) REFERENCES professor (professor_id)
);




CREATE TABLE Student (
  student_id int NOT NULL,
  first_name varchar(50),
  last_name varchar(50),
  birth_date timestamp,
  login varchar(50),
  section_id int,
  year_result int,
  course_id varchar(6) NOT NULL,
  CONSTRAINT PK_student PRIMARY KEY (student_id),
  constraint FK_student_section foreign key (section_id) references section (section_id)
);

CREATE TABLE Grade (
-- ATTENTION :, La table est la source de vérité, ne pas la modifier pour l'ajout de données qui ne respectent pas les contraintes
  grade char(2) NOT NULL check (grade IN ('E','TB','B','S','F','I','IG')),
  lower_bound int NOT NULL,
  upper_bound int NOT NULL,
  CONSTRAINT PK_grade PRIMARY KEY (grade)
);