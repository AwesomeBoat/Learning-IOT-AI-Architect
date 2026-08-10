-- # Module 11 — Sous-requêtage & Fonctions de fenêtrage — Exercices (stagiaires)

-- Base utilisée : Northwind (`products`, `categories`, `orders`, `order_details`, `customers`).

-- ## Partie 1 — Sous-requêtage

-- ### Exercice 1 — Produits les plus chers par catégorie
-- Récupérer, pour chaque catégorie de `categories`, le ou les produits de
-- `products` dont le `unit_price` est le plus élevé de la catégorie.


SELECT *
FROM categories

SELECT *
FROM products

SELECT C.category_name, P.product_name, P.unit_price
FROM categories AS C
JOIN products AS P ON P.category_id = C.category_id
WHERE P.unit_price = (
	SELECT MAX(P2.unit_price)
	FROM products AS P2
	WHERE P2.category_id = P.category_id
)
	ORDER BY c.category_name, P.product_name

-- CORRECTION

SELECT category_name
FROM categories AS C
LEFT JOIN(
	SELECT MAX(unit_price) AS Maximum
	FROM products AS P
	WHERE P.category_id = C.category_id
) AS X
-- ### Exercice 2 — Vue clients dynamique avec segmentation
-- Créer une vue `v_clients_segmentation` contenant : `customer_id`,
-- `company_name`, `contact_name`, le nombre de commandes passées par le
-- client, et un flag `segment` valant `'Top client'` si le client a passé
-- plus de commandes que la moyenne des autres clients, sinon
-- `'Client standard'`. Ajouter une colonne `anciennete_jours` correspondant
-- au nombre de jours entre la date de sa première commande et aujourd'hui.

-- Nombres de commandes par client

SELECT
	customer_id,
	COUNT(*) AS nb_commandes
FROM orders
GROUP BY customer_id;

-- Date de la première commande pour chaque clients

SELECT
	customer_id,
	MIN(order_date) AS premiere_commande
FROM orders
GROUP BY customer_id


-- Moyenne des commandes par client
SELECT
	AVG(nb_commandes) AS moyenne_commandes
	FROM(
		SELECT
			customer_id,
			COUNT(*) AS nb_commandes
		FROM orders
		GROUP BY customer_id
	)


-- Case de segmentation top client
CASE 
	WHEN nb_commandes > moyenne_commandes
	THEN 'Top client'
	ELSE 'Client standart'
END


-- Calculer l'ancienneté
CURRENT_DATE - premiere_commandes


--- CREATION DE LA VUE
CREATE OR REPLACE VIEW v_clients_segmentation AS
WITH stats_clients AS (
    SELECT
        customer_id,
        COUNT(*) AS nb_commandes,
        MIN(order_date) AS premiere_commande
    FROM orders
    GROUP BY customer_id
),
moyenne AS (
    SELECT AVG(nb_commandes) AS moyenne_commandes
    FROM stats_clients
)
SELECT
    c.customer_id,
    c.company_name,
    c.contact_name,
    s.nb_commandes,
    CASE
        WHEN s.nb_commandes > m.moyenne_commandes
            THEN 'Top client'
        ELSE 'Client standard'
    END AS segment,
    CURRENT_DATE - s.premiere_commande::date AS anciennete_jours
FROM customers c
JOIN stats_clients s
    ON c.customer_id = s.customer_id
CROSS JOIN moyenne m;

SELECT *
FROM v_clients_segmentation


-- EX 2 CORRECTION ---------------

SELECT customer_id, contact_name, company_name
FROM customers AS C

SELECT COUNT(*) AS nbre_commandes, O.customer_id
FROM orders AS O
LEFT JOIN customers AS C ON C.customer_id = O.customer_id
GROUP BY O.customer_id,C.contact_name, C.company_name

-- Calcul de la moyenne de commandes
SELECT AVG(tot_client)
FROM
(
	SELECT COUNT(*) AS tot_client, customer_id
	FROM orders
	GROUP BY customer_id
) AS X
------ Calcul de la moyenne autre manière

SELECT COUNT(*) :: FLOAT / COUNT(DISTINCT customer_id)
FROM orders

WITH base AS 
(
	SELECT
		COUNT(*) AS nb,
		CURRENT_DATE - MIN(order_date) Anciennete(jours),
		O.customer_id,
		C.contact_name,
		C.company_name,
		(SELECT COUNT(*) :: FLOAT / COUNT(DISTINCT customer_id) FROM orders) AS moyenne_tot
	FROM
		orders AS O
	INNER JOIN customers AS C ON C.customer_id = O.customer_id
	GROUP BY O.customer_id, C.contact_name, C.company_name
)
SELECT *,
	CASE
		WHEN nb > moyenne_tot THEN 'GOLDEN CLIENT'
		WHEN nb < moyenne_tot THEN 'STINGY B*TCH'
		WHEN nb = moyenne_tot THEN 'MHH IDK'
	END AS flag
FROM base

------------ FIN CORRECTION EX 2 ----------------



-- WINDOWS FUNCTION (Fonction de fenêtrage)    OVER () AS nom permet de ne pas utiliser le GROUP BY lors d'une AGGR dans select
SELECT *, 
	AVG(unit_price) OVER () AS moy_de_tout,
	units_in_stock :: FLOAT / SUM(units_in_stock) OVER () AS pct_du_stock_global
FROM products


SELECT * 
FROM(
	SELECT product_id,
		product_name,
		unit_price,
		category_id,
		RANK() OVER(PARTITION BY category_id ORDER BY unit_price DESC) AS rk -- RANK()
	FROM products
) AS X
WHERE rk <= 3
ORDER BY rk



SELECT 
	customer_id,
	order_date,
	LAG(order_date, 1) OVER(PARTITION BY customer_id ORDER BY order_date ASC ) AS date_prec,
	order_date - LAG(order_date, 1) OVER(PARTITION BY customer_id ORDER BY order_date ASC ) AS diff_date
FROM orders
ORDER BY customer_id, order_date ASC

-- ### Exercice 3 — Produits : prix catalogue vs dernier prix pratiqué
-- Récupérer tous les produits distincts avec :
-- a. leur id, nom et catégorie (si NULL, remplacer par `'NA'`) — *adaptation :
-- Northwind n'ayant pas de sous-catégorie, on ne garde qu'un seul niveau de
-- catégorie.* 
-- b. leur `unit_price` (prix catalogue actuel).
-- c. le dernier prix pratiqué pour ce produit dans `order_details` (celui de
-- la commande la plus récente) — 
-- d. une colonne calculant la différence entre les deux, pour vérifier s'il y
-- en a une.

-- ### Exercice 4 — Quantités et montants vendus, par année et catégorie
-- *Adaptation : Northwind n'a pas de schéma d'achats (`Purchasing`) comme
-- AdventureWorks ; l'exercice compare donc deux mesures de vente.*
-- Faire une requête qui donne, pour toutes les années et catégories de
-- produit : le total des quantités vendues, et le total du montant vendu
-- (`quantity * unit_price * (1 - discount)`). La table doit compter 4
-- colonnes : Année, Catégorie, Total Quantité, Total Montant.

-- ### Exercice 5 — Évolution des quantités commandées, mois par mois vs N-1
-- Faire une table donnant, pour chaque année et chaque mois : le total des
-- quantités commandées (`quantity`), le total de l'année précédente pour ce
-- même mois, et la différence entre les deux en valeur brute et en
-- pourcentage.

-- ## Partie 2 — Fonctions de fenêtrage

-- ### Exercice 1 — Top 10 des produits par quantité vendue
-- *Adaptation : Northwind ne distingue pas les canaux de vente (pas de flag
-- "en ligne" comme dans AdventureWorks) ; on classe donc l'ensemble des
-- ventes.*
-- Classer les produits selon leur quantité totale vendue (créer une colonne
-- de classement) et ne récupérer que les 10 meilleurs.

-- ### Exercice 2 — Cumul des ventes par jour, réinitialisé chaque année
-- Calculer le montant total des ventes par jour de commande, puis un total
-- cumulé de ce montant qui doit se réinitialiser à chaque nouvelle année.

-- ### Exercice 3 — Part de marché de chaque produit
-- Calculer la part (en %) de chaque produit dans le total des ventes.
-- Calculer également sa part (en %) au sein des ventes de sa propre
-- catégorie.

-- ### Exercice 4 — Ventes du jour vs moyenne mobile des 3 jours précédents
-- Calculer le montant des ventes par jour, et déterminer si ce montant est
-- au-dessus ou en dessous de la moyenne des 3 jours précédents. Créer un
-- flag pour l'indiquer.

-- ### Exercice 5 — Délai moyen entre deux commandes par client
-- Pour chaque client, calculer le temps moyen (en jours) entre deux
-- commandes consécutives. Si le client n'a passé qu'une seule commande, la
-- valeur doit être NULL.

-- ### Exercice 6 — Vue Pareto des ventes par catégorie de produit
-- *Adaptation : pas de sous-catégorie dans Northwind, on utilise la
-- catégorie.*
-- Créer une vue permettant de tracer facilement une courbe de Pareto des
-- ventes par catégorie de produit. La vue doit contenir la catégorie, le
-- total des ventes, ainsi que le pourcentage cumulé des ventes, trié du plus
-- vendu au moins vendu.
