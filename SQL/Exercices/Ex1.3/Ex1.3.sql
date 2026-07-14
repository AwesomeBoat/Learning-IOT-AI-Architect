-- Database: test

-- DROP DATABASE IF EXISTS test;

CREATE TABLE T_taux_tva(
id_taux INT,
pourcentage_taux INT,
CONSTRAINT PK_taux_tva PRIMARY KEY (id_taux)
);


CREATE TABLE T_rayon_ryn(
nom_rayon VARCHAR(30),
CONSTRAINT PK_nom_rayon PRIMARY KEY (nom_rayon)
);

CREATE TABLE T_fabriquant_fbq(
id_fabriquant INT,
CONSTRAINT PK_id_fabriquant PRIMARY KEY (id_fabriquant)
);


CREATE TABLE T_produit_pdt(
identifiant INT PRIMARY KEY,
ref_magasin VARCHAR(20),
ref_fabriquant INT,
code_ean13 INT,
prix_de_vente FLOAT NOT NULL,
ref_nom_rayon VARCHAR(20),
CONSTRAINT FK_produit_fabriquant FOREIGN KEY (ref_fabriquant)
REFERENCES T_fabriquant_fbq(id_fabriquant),
CONSTRAINT ref_codeean_unique UNIQUE (code_ean13),
CONSTRAINT FK_T_produit_T_rayon FOREIGN KEY (ref_nom_rayon)
REFERENCES T_rayon_ryn(nom_rayon)
);


