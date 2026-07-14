

--Autoriser la table « SECTION » à accepter des valeurs NULL pour la colonne 
--« delegate_id »

ALTER TABLE section DROP COLUMN delegate_id;
ALTER TABLE section ADD COLUMN delegate_id int;


--Ajouter à la table « SECTION » une clé étrangère faisant pointer la colonne 
--« delegate_id » vers la colonne « student_id » de la table « STUDENT » 

ALTER TABLE section ADD CONSTRAINT FK_delegate_id FOREIGN KEY (delegate_id) REFERENCES student(student_id);

--Supprimer la colonne « course_id » de la table « STUDENT » 
ALTER TABLE student DROP COLUMN course_id;

--Faire en sorte que les données de la colonne « student_id » de la table 
--« STUDENT » soient auto-incrémentées 

ALTER TABLE student ALTER COLUMN student_id ADD GENERATED ALWAYS AS IDENTITY;


--En ne supprimant aucune donnée, modifier le type de la colonne « section_id » de 
--la table « section » afin qu’il soit en CHAR(4). Cela impliquera peut-être d’autres 
--modifications…

-- SUPPRIMER LES CONTRAINTES DES TABLES EXTERNES QUI POINTENT VERS section_id
ALTER TABLE professor DROP CONSTRAINT FK_professor_section;
ALTER TABLE student DROP CONSTRAINT FK_student_section;

-- ALTERER LE TYPE DE section_id 
ALTER TABLE section ALTER COLUMN section_id TYPE char(4);

-- ALTER LE Type de section_id dans mes tables qui l'utilisent comme FK
ALTER TABLE professor ALTER COLUMN section_id  TYPE char(4);
ALTER TABLE student ALTER COLUMN section_id TYPE char(4);

-- RAJOUTER LES FK
ALTER TABLE professor ADD CONSTRAINT FK_professor_section foreign key (section_id) references section (section_id);
ALTER TABLE student ADD CONSTRAINT FK_student_section FOREIGN KEY (section_id) REFERENCES section (section_id);

