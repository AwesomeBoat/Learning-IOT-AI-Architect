# FastAPI — Jour 1

## Créer une API REST en Python

Objectif de la journée : comprendre ce qu'est une API, comment fonctionne HTTP, et construire une petite API CRUD complète avec FastAPI.

Fil rouge : l'API d'un label de musique — **Noise Records**.

---

## Comment on va travailler aujourd'hui

L'API du label gère deux ressources principales : les **artistes** et les **albums**.

La journée fonctionne en binôme :

```text
DÉMO                     →  ressource artists
EXERCICE de votre côté   →  ressource albums
```

Chaque fois qu'on voit une notion, je la construis devant vous sur `artists`. Ensuite vous l'appliquez vous-mêmes sur `albums`, dans le même fichier. Ce n'est pas du copier-coller : les données sont différentes, les champs sont différents, et vous rencontrerez des problèmes que je n'aurai pas eus.

À la fin de la journée, `artists` sera l'API qu'on a écrite ensemble, et `albums` sera **la vôtre**. Et si vous êtes rapides, il y a une troisième ressource à construire de zéro.

---

# 1. Comprendre ce qu'est une API avant d'écrire du code

## 1.1 Le problème de base

Vous avez une application (un site web, une app mobile, un logiciel). Elle a besoin de données : la liste des artistes du label, les albums, les ventes. Ces données ne sont pas dans le navigateur de l'utilisateur, elles sont sur un serveur quelque part.

Il faut donc un moyen pour que l'application **demande** ces données, et que le serveur **réponde**.

Ce moyen, c'est une API.

```text
Frontend / application mobile / Postman
                |
                | requête HTTP
                v
               API
                |
                | données / logique
                v
             serveur
```

## 1.2 Le vocabulaire minimum

**Client** : celui qui demande. Un navigateur, une app mobile, un script Python, Postman, l'onglet `/docs` de FastAPI. Le client ne connaît pas la base de données, il ne connaît que l'adresse de l'API.

**Serveur** : celui qui répond. C'est la machine (ou le processus) qui contient les données et le code métier.

**API** (*Application Programming Interface*) : le contrat entre les deux. C'est la liste des choses qu'on peut demander et la façon de les demander. Une API n'est pas forcément liée au web — une bibliothèque Python expose aussi une API — mais aujourd'hui on parle d'API **Web**.

**API Web** : une API accessible via HTTP, à des adresses de type `http://localhost:8000/artists`.

**HTTP** : le protocole de communication du web. Un protocole, c'est juste un ensemble de règles sur la forme des messages : comment on écrit une demande, comment on écrit une réponse. Le client envoie une **requête**, le serveur renvoie une **réponse**. Un aller, un retour, et c'est terminé.

**JSON** : le format texte utilisé pour transporter les données. Ça ressemble beaucoup à un dictionnaire Python, et c'est lisible par n'importe quel langage.

## 1.3 Un exemple concret

Le client demande l'artiste numéro 1 :

```http
GET /artists/1
```

Le serveur répond :

```json
{
    "id": 1,
    "name": "Metallica",
    "genre": "Metal"
}
```

C'est tout. Une API, c'est fondamentalement ça : des adresses qu'on appelle, et du JSON qui revient.

Le reste de la journée consiste à comprendre chaque partie de cet échange, et à écrire le code Python qui produit ce genre de réponse.

## 1.4 Ce qu'une API n'est pas

Une API ne renvoie pas par defaut de HTML, pas de CSS, pas de page à afficher. Elle renvoie **des données**. C'est le client qui décide comment les afficher. C'est justement l'intérêt : la même API peut servir un site web, une app mobile et un dashboard interne.

---

# 2. Introduction à REST

REST est un **style** de conception d'API Web. Il n'y a rien à installer, rien à importer : ce sont des conventions sur la façon de nommer les adresses et d'utiliser HTTP.

## 2.1 L'idée centrale : la ressource

Dans une API REST, on ne raisonne pas en termes d'actions mais en termes de **ressources**. Une ressource, c'est un type de chose que l'API gère :

```text
artists
albums
members
```

Chaque ressource a une adresse (une **URL**), et on utilise la **méthode HTTP** pour dire ce qu'on veut faire dessus.

```http
GET    /artists          récupérer tous les artistes
GET    /artists/3        récupérer l'artiste 3
POST   /artists          créer un artiste
PATCH  /artists/3        modifier l'artiste 3
DELETE /artists/3        supprimer l'artiste 3
```

L'URL dit **quoi**, la méthode dit **quelle opération**.

## 2.2 Pourquoi pas l'autre approche ?

On pourrait très bien écrire une API comme ça :

```text
/getAllArtists
/getArtist?id=3
/createArtist
/deleteArtist
```

Ça marche techniquement. Mais :

- le verbe est déjà dans la méthode HTTP, on le répète pour rien ;
- il faut deviner ou lire la doc pour chaque nouvelle adresse ;
- rien n'est prévisible : `getAllArtists`, `listAlbums`, `fetchMembers`... chaque développeur invente son style ;
- on perd les mécanismes standards de HTTP (cache, codes de statut, idempotence).

Avec REST, dès que quelqu'un connaît `/artists`, il devine `/albums`. C'est le vrai bénéfice : la **prévisibilité**. Et c'est aussi pour ça que vous allez pouvoir écrire l'API `albums` aujourd'hui sans que je vous la dicte.

## 2.3 CRUD et HTTP

CRUD = les quatre opérations de base sur des données. La correspondance habituelle :

| Action | CRUD | HTTP |
| --- | --- | --- |
| récupérer | Read | GET |
| créer | Create | POST |
| remplacer | Update | PUT |
| modifier partiellement | Update | PATCH |
| supprimer | Delete | DELETE |

Point important : **ce sont des conventions, pas de la magie FastAPI**. Rien n'empêche techniquement d'écrire une route `GET /deleteArtist` qui supprime des données. Ce serait juste une très mauvaise idée, et tous les outils autour (cache navigateur, proxies, clients HTTP) partent du principe que GET ne modifie rien.

---

# 3. Anatomie simple d'une requête HTTP

Regardons une requête complète, celle qui crée un artiste :

```http
POST /artists
Content-Type: application/json

{
    "name": "Gorillaz",
    "genre": "Alternative"
}
```

Trois parties :

- **la méthode** : `POST`. L'intention.
- **le path** : `/artists`. La ressource visée.
- **les headers** : `Content-Type: application/json`. Des métadonnées sur la requête. Ici : « le contenu que j'envoie est du JSON ». C'est aussi là que passeront plus tard les tokens d'authentification.
- **le body** : le JSON. Les données envoyées. Un GET n'a normalement pas de body, un POST oui.

La réponse a la même structure, avec un **code de statut** en plus :

```http
201 Created
Content-Type: application/json
```

```json
{
    "id": 6,
    "name": "Gorillaz",
    "genre": "Alternative",
    "active": true
}
```

- **le code de statut** : `201`. Un nombre qui résume ce qui s'est passé. On y revient en détail cet après-midi.
- **les headers** de réponse.
- **le body** de réponse : les données renvoyées.

---

# 4. Installation et premier projet

## 4.1 Environnement virtuel

On crée un dossier de projet, puis un environnement virtuel dedans :

```bash
mkdir music-label-api
cd music-label-api
python -m venv .venv
```

Activation :

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell - CMD
.venv\Scripts\activate
```

Le nom de l'environnement doit apparaître dans le prompt du terminal. Si ce n'est pas le cas, `pip install` va installer les paquets globalement, et ça finit toujours mal.

## 4.2 Installation

```bash
pip install "fastapi[standard]"
```

Les guillemets sont nécessaires dans certains shells à cause des crochets. `[standard]` installe FastAPI **et** ce qui va autour : le serveur Uvicorn, la CLI `fastapi`, et quelques dépendances utiles.

## 4.3 Premier fichier

Créez `main.py` :

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Music Label API"}
```

## 4.4 Lancement

```bash
fastapi dev main.py
```

Trois adresses à ouvrir tout de suite :

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

La première renvoie le JSON. Les deux autres sont de la documentation générée automatiquement — on y revient juste après.

## 4.5 Le code, ligne par ligne

```python
app = FastAPI()
```

On crée l'application. C'est l'objet qui va contenir toutes les routes. Il n'y en a qu'un par projet, et par convention on l'appelle `app`.

```python
@app.get("/")
```

Un décorateur. Il dit à FastAPI : « quand une requête `GET` arrive sur le path `/`, appelle la fonction juste en dessous ». La méthode HTTP est dans le nom du décorateur (`app.get`, `app.post`, `app.patch`, `app.delete`), le path est dans les parenthèses.

```python
def root():
```

Une fonction Python normale. Son nom n'a aucune importance pour le client : il ne sert qu'à vous, dans le code. Ce qui compte, c'est le décorateur au-dessus.

```python
return {"message": "Welcome to Music Label API"}
```

On retourne un dictionnaire Python. FastAPI le convertit automatiquement en JSON et l'envoie avec le header `Content-Type: application/json`. Pas besoin d'appeler `json.dumps()`.

## 4.6 Et Uvicorn dans tout ça ?

FastAPI est un **framework** : il vous aide à écrire des routes et à valider des données. Mais il n'écoute pas sur un port réseau.

Ce travail-là, c'est celui du **serveur** : Uvicorn. Il ouvre le port 8000, reçoit les requêtes HTTP brutes, les passe à votre application FastAPI, récupère la réponse et la renvoie au client.

`fastapi dev main.py` lance Uvicorn en mode développement, avec le rechargement automatique : dès que vous sauvegardez `main.py`, le serveur redémarre. Gardez le terminal visible, les erreurs s'affichent dedans.

---

# 5. Swagger et OpenAPI

Ouvrez `http://127.0.0.1:8000/docs`.

Vous avez une page interactive qui liste vos routes, avec un bouton « Try it out » pour les exécuter. Et vous n'avez rien écrit pour ça.

Ce qu'il faut comprendre : **ce n'est pas une fonctionnalité qu'on code route par route**. FastAPI lit votre code et en déduit une description de votre API au format **OpenAPI** (un standard, du JSON — allez voir `http://127.0.0.1:8000/openapi.json`). **Swagger UI**, la page `/docs`, n'est qu'une interface graphique qui affiche ce JSON.

Pour construire cette description, FastAPI utilise :

- les routes (méthode + path) ;
- les annotations de type de vos paramètres de fonction ;
- les modèles Pydantic (on les voit cet après-midi).

Autrement dit : plus votre code est correctement typé, plus la documentation est précise. C'est le même travail qui sert à la validation et à la doc.

Concrètement, ça remplace Postman pour la journée. À chaque nouvelle route, on va tester dans `/docs`.

---

# 6. Exercice 1 — Premières routes

**Temps : 15 minutes.**

Cet exercice-ci est de la pure mise en jambes, on refait ensemble ce que vous venez de voir. Les suivants seront plus intéressants.

Ajoutez trois routes GET dans `main.py` :

| Route | Réponse attendue |
| --- | --- |
| `GET /` | `{"message": "Welcome to Music Label API"}` (déjà fait) |
| `GET /health` | `{"status": "ok"}` |
| `GET /label` | `{"name": "Noise Records", "country": "Belgium"}` |

Consignes :

1. Chaque route a son propre décorateur et sa propre fonction.
2. Testez les trois dans `/docs`.
3. Vérifiez aussi dans le navigateur directement (`http://127.0.0.1:8000/health`).

---

# 7. Mock data et première vraie ressource

## 7.1 Les deux jeux de données

On ajoute les données du label, sous forme de listes de dictionnaires, juste après `app = FastAPI()` :

```python
artists = [
    {"id": 1, "name": "Metallica", "genre": "Metal", "country": "US", "active": True},
    {"id": 2, "name": "Linkin Park", "genre": "Rock", "country": "US", "active": True},
    {"id": 3, "name": "Eminem", "genre": "Rap", "country": "US", "active": True},
    {"id": 4, "name": "Daft Punk", "genre": "Electronic", "country": "FR", "active": False},
    {"id": 5, "name": "Adele", "genre": "Pop", "country": "UK", "active": True},
]

albums = [
    {"id": 1, "title": "Master of Puppets", "artist_id": 1, "year": 1986},
    {"id": 2, "title": "The Black Album", "artist_id": 1, "year": 1991},
    {"id": 3, "title": "Hybrid Theory", "artist_id": 2, "year": 2000},
    {"id": 4, "title": "Meteora", "artist_id": 2, "year": 2003},
    {"id": 5, "title": "The Marshall Mathers LP", "artist_id": 3, "year": 2000},
    {"id": 6, "title": "Discovery", "artist_id": 4, "year": 2001},
    {"id": 7, "title": "Random Access Memories", "artist_id": 4, "year": 2013},
    {"id": 8, "title": "21", "artist_id": 5, "year": 2011},
]
```

Points à relever :

- ce sont des **listes Python normales**, rien de spécifique à FastAPI ;
- elles jouent temporairement le rôle de **stockage** : c'est là qu'on lit et qu'on écrit ;
- chaque élément a un `id` unique, qui va servir à le cibler dans les URLs ;
- `artist_id` dans un album est une **référence** vers un artiste. C'est le début d'une relation entre deux ressources — on l'exploitera cet après-midi ;
- Daft Punk a `active: False`, le groupe a splitté. Ça nous donnera un filtre intéressant.

Et surtout : **ce n'est pas une base de données**. Ces listes vivent dans la mémoire du processus Python. On y reviendra explicitement en début d'après-midi, quand on aura créé des données.

**Rappel du fonctionnement de la journée** : je travaille sur `artists`, vous travaillez sur `albums`. Les deux listes sont là dès maintenant, ne touchez pas encore à `albums`.

## 7.2 La route collection

```python
@app.get("/artists")
def get_artists():
    return artists
```

Testez `/artists` dans `/docs`.

FastAPI a converti la liste de dictionnaires en tableau JSON. Là encore, aucune conversion manuelle : les types Python de base (dict, list, str, int, bool, None) ont un équivalent JSON direct.

Cette route s'appelle une route « collection » : elle renvoie **tous** les éléments de la ressource.

---

# 8. Path parameters

## 8.1 Le besoin

`/artists` renvoie tout. Mais un client veut souvent **un** artiste précis. On ne va pas créer une route par artiste. Il faut une partie variable dans l'URL.

```python
@app.get("/artists/{artist_id}")
def get_artist(artist_id: int):
    for artist in artists:
        if artist["id"] == artist_id:
            return artist
    return {"error": "Artist not found"}
```

## 8.2 Décomposition

```text
/artists/{artist_id}
```

Les accolades déclarent un **path parameter** : un segment variable de l'URL. FastAPI va extraire ce segment et le passer à la fonction.

```python
def get_artist(artist_id: int):
```

Le nom du paramètre de la fonction **doit** correspondre au nom entre accolades. C'est comme ça que FastAPI fait le lien.

Le `: int` est la partie intéressante. Dans une URL, tout est du texte : `/artists/1` transporte la chaîne `"1"`, pas l'entier `1`. En annotant `int`, vous dites à FastAPI :

1. convertis-moi ça en entier ;
2. si ce n'est pas convertible, refuse la requête.

## 8.3 Les tests à faire ensemble

```text
/artists/1     -> Metallica
/artists/3     -> Eminem
/artists/99    -> {"error": "Artist not found"}
/artists/test  -> erreur 422
```

Le dernier est le plus important. Regardez la réponse :

```json
{
    "detail": [
        {
            "type": "int_parsing",
            "loc": ["path", "artist_id"],
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "input": "test"
        }
    ]
}
```

Votre fonction n'a **jamais été appelée**. FastAPI a validé l'entrée avant, et a renvoyé une erreur détaillée : à quel endroit (`path`, `artist_id`), quel problème, quelle valeur reçue.

Enlevez le `: int` et refaites le test : `/artists/test` passe maintenant dans la fonction, et vous comparez une chaîne avec des entiers, donc vous ne trouvez jamais rien. Remettez-le.

## 8.4 Le point à retenir de la journée

> FastAPI utilise énormément les annotations de type Python pour comprendre, convertir et valider les données.

Dans la plupart des frameworks, le typage est décoratif — un commentaire pour l'éditeur. Ici, il pilote le comportement réel : la validation, la conversion, la documentation, les messages d'erreur. C'est le concept central de FastAPI.

## 8.5 Sur le `return {"error": ...}`

Notre gestion du « pas trouvé » est bancale : on renvoie un message d'erreur avec un code de statut `200 OK`. Pour le client, la requête a donc réussi. Ce n'est pas correct.

On corrige ça cet après-midi avec `HTTPException`, une fois qu'on aura vu les codes de statut. Pour l'instant, on avance.

---

# 9. Query parameters

## 9.1 Path ou query ?

Comparez :

```http
GET /artists/3
GET /artists?genre=Metal
```

Le premier **cible une ressource précise**. Il y a un artiste 3, je le veux, lui.

Le second **filtre une collection**. Je veux la liste des artistes, mais pas tous.

La règle pédagogique, à retenir telle quelle :

- **path parameter** = identifier / cibler une ressource ;
- **query parameter** = filtrer / trier / configurer la requête.

Un query parameter est toujours **optionnel** par nature : `/artists` sans rien doit continuer à fonctionner.

## 9.2 Déclaration

En FastAPI, la différence est simple : si le nom du paramètre de fonction apparaît entre accolades dans le path, c'est un path parameter. Sinon, c'est un query parameter.

```python
@app.get("/artists")
def get_artists(genre: str | None = None):
    if genre is None:
        return artists

    return [
        artist
        for artist in artists
        if artist["genre"].lower() == genre.lower()
    ]
```

`str | None = None` veut dire : c'est une chaîne, ou rien, et par défaut c'est rien. La valeur par défaut rend le paramètre optionnel.

Le `.lower()` des deux côtés évite que `?genre=metal` ne renvoie rien.

Tests :

```text
/artists
/artists?genre=Metal
/artists?genre=rap
/artists?genre=Jazz          -> []
```

Une liste vide n'est pas une erreur. La requête est valide, il n'y a simplement aucun résultat. On renvoie `[]` avec un `200`, pas un `404`.

## 9.3 Plusieurs filtres

On ajoute `active`, et on restructure pour ne pas empiler les `if/else` :

```python
@app.get("/artists")
def get_artists(
    genre: str | None = None,
    active: bool | None = None,
):
    result = artists

    if genre is not None:
        result = [
            artist
            for artist in result
            if artist["genre"].lower() == genre.lower()
        ]

    if active is not None:
        result = [
            artist
            for artist in result
            if artist["active"] == active
        ]

    return result
```

Le pattern est classique et se lit bien : on part de tout, et chaque filtre présent réduit le résultat. Retenez-le, il vous servira dans vingt minutes.

Attention au piège du `if genre:` au lieu de `if genre is not None:`. Avec `active`, `if active:` ignorerait complètement `?active=false`, puisque `False` est falsy. Testez les deux versions, ça marque les esprits.

Tests :

```text
/artists?active=true         -> tout sauf Daft Punk
/artists?active=false        -> Daft Punk
/artists?genre=Rock&active=true
```

Notez la conversion : dans l'URL vous écrivez le texte `true`, votre fonction reçoit le booléen Python `True`. Là encore, c'est l'annotation `bool` qui déclenche ça. FastAPI accepte `true`, `false`, `1`, `0`, `yes`, `no`. Essayez `?active=maybe` : 422.

Le champ `country` fonctionnerait exactement de la même façon (`?country=FR`) — c'est trois lignes de plus, sur le même modèle. Je vous le laisse si vous voulez le tester.

## 9.4 Un paramètre de configuration

Tous les query parameters ne sont pas des filtres :

```python
@app.get("/artists")
def get_artists(
    genre: str | None = None,
    active: bool | None = None,
    limit: int | None = None,
):
    result = artists

    if genre is not None:
        result = [
            artist
            for artist in result
            if artist["genre"].lower() == genre.lower()
        ]

    if active is not None:
        result = [
            artist
            for artist in result
            if artist["active"] == active
        ]

    if limit is not None:
        result = result[:limit]

    return result
```

`?limit=2` ne filtre pas sur le contenu, il configure la réponse. C'est le début de la pagination, qu'on ne fera pas aujourd'hui.

Allez voir `/docs` : les trois paramètres sont documentés, avec leur type et le fait qu'ils sont optionnels. Toujours sans écrire une ligne de documentation.

---

# 10. Exercice 2 — La lecture des Albums

**Temps : 40 minutes.**

À vous. Vous avez vu comment on lit une collection, comment on cible un élément par son id, et comment on filtre avec des query parameters. Appliquez tout ça à la ressource `albums`.

Ne recopiez pas le code de `artists` en remplaçant les mots : les champs ne sont pas les mêmes, et deux des filtres demandés n'existent pas dans la démo.

## Obligatoire

**1.** La route collection :

```http
GET /albums
```

**2.** La route de détail :

```http
GET /albums/{album_id}
```

Si l'album n'existe pas, renvoyez pour l'instant `{"error": "Album not found"}` — on verra la façon propre de faire ça après la pause.

**3.** Quatre query parameters sur `/albums` :

```http
GET /albums?artist_id=1
GET /albums?year=2003
GET /albums?min_year=2000
GET /albums?max_year=2010
```

`min_year` et `max_year` ne sont pas des égalités : ce sont des comparaisons. Réfléchissez à l'opérateur.

**4.** Les filtres doivent être **combinables** :

```http
GET /albums?artist_id=1&min_year=1990
GET /albums?artist_id=4&max_year=2010
GET /albums?min_year=2000&max_year=2005
```

Vérifiez vos résultats à la main dans la mock data avant de crier au bug.

**5.** Une route de comptage :

```http
GET /albums/count
```

```json
{
    "count": 8
}
```

## Bonus

**6.** Une recherche par titre partiel, insensible à la casse :

```http
GET /albums/search?title=the
GET /albums/search?title=met
```

**7.** Un filtre `?sort=year` sur `/albums` qui renvoie les albums triés par année.

## Un avertissement

Pour les points 5 et 6, testez la route **immédiatement** après l'avoir écrite. Si vous obtenez un `422` là où vous attendiez un résultat, ne changez pas tout : lisez le message d'erreur, regardez le champ `loc`, et demandez-vous quelle route FastAPI a réellement exécutée.

Utilisez vos bases Python : boucles, `if`, compréhensions de listes, `in`, `.lower()`, `sorted()`.

---

# 11. Request body

## 11.1 Envoyer des données au serveur

Jusqu'ici on a seulement lu. Pour créer un artiste, le client doit **envoyer** des données.

Première idée qui vient : les mettre dans l'URL.

```text
POST /artists?name=Daft%20Punk&genre=Electronic&active=false
```

Ça fonctionnerait, mais c'est une mauvaise idée :

- l'URL a une longueur limitée en pratique ;
- il faut encoder les caractères spéciaux (`%20` pour un espace, et bonjour les accents) ;
- une URL est structurellement plate : impossible d'envoyer un objet imbriqué ou une liste ;
- les URLs sont loguées partout, y compris avec leurs paramètres ;
- et surtout : conceptuellement, un query parameter configure une requête, il ne transporte pas le contenu d'une ressource.

## 11.2 Le body

On envoie donc les données dans le **body** de la requête, en JSON :

```http
POST /artists
Content-Type: application/json

{
    "name": "Gorillaz",
    "genre": "Alternative",
    "country": "UK",
    "active": true
}
```

Plus de limite de taille pratique, structure libre, pas d'encodage exotique.

Mais un nouveau problème apparaît : ce body vient de l'extérieur. Rien ne garantit qu'il contienne `name`. Rien ne garantit que `active` soit un booléen. Rien ne garantit que ce soit même du JSON valide.

Il faut donc **valider**. Et c'est là qu'arrive Pydantic.

---

# 12. Pydantic

## 12.1 Déclarer la forme attendue

```python
from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str
    genre: str
    country: str
    active: bool = True
```

Puis :

```python
@app.post("/artists")
def create_artist(artist: ArtistCreate):
    return artist
```

Testez dans `/docs`. Vous avez un formulaire, avec un exemple de body pré-rempli et le détail des champs attendus.

## 12.2 Ce qui se passe exactement

**Pourquoi une classe ?** Parce qu'on décrit une **forme de données** : quels champs, de quels types, obligatoires ou non. Une classe avec des annotations est la façon la plus lisible d'exprimer ça en Python.

**`BaseModel`** est la classe de base de Pydantic. En héritant d'elle, votre classe gagne toute la machinerie de validation et de conversion. Vous n'écrivez que la description.

**Les types font le travail.** `name: str` signifie : champ obligatoire, de type chaîne. `active: bool = True` signifie : champ optionnel, booléen, valeur par défaut `True` si absent.

Petit détail Python qui va vous rattraper : les champs avec valeur par défaut doivent venir **après** ceux qui n'en ont pas. C'est la même règle que pour les paramètres de fonction.

**FastAPI reconnaît le modèle.** Quand un paramètre de fonction est annoté avec un modèle Pydantic, FastAPI ne va pas le chercher dans les query parameters : il comprend qu'il s'agit du **body**. C'est la même règle que tout à l'heure — le type détermine le comportement :

| Annotation du paramètre | Origine de la valeur |
| --- | --- |
| nom présent dans le path | path parameter |
| type simple (`int`, `str`, `bool`) | query parameter |
| modèle Pydantic | request body (JSON) |

**Ce que fait Pydantic à l'arrivée** :

1. il lit le JSON ;
2. il vérifie que les champs obligatoires sont là ;
3. il convertit ce qui est convertible (`"1991"` vers `1991` pour un `int`) ;
4. il refuse ce qui ne l'est pas, avec un message précis ;
5. il vous donne un **objet Python typé**, pas un dictionnaire brut.

Votre fonction n'est appelée que si tout est valide. Vous n'avez aucun `if "name" not in body` à écrire.

## 12.3 Manipuler l'objet reçu

`artist` est une instance de `ArtistCreate`. On accède aux champs par attribut, pas par clé :

```python
artist.name       # "Gorillaz"
artist.genre      # "Alternative"
artist.active     # True

artist["name"]    # TypeError
```

Bonus immédiat : l'autocomplétion fonctionne dans l'éditeur, et une faute de frappe sur `artist.nmae` est détectée sans lancer le serveur.

Pour repasser à un dictionnaire — ce dont on va avoir besoin, puisque notre stockage est une liste de dicts :

```python
artist.model_dump()
# {"name": "Gorillaz", "genre": "Alternative", "country": "UK", "active": True}
```

`model_dump()` est la syntaxe Pydantic v2. Vous trouverez énormément de tutoriels avec `.dict()` : c'est l'ancienne API (Pydantic v1), dépréciée. Même chose pour `.json()`, remplacé par `model_dump_json()`.

---

# 13. Voir les erreurs de validation

C'est le moment le plus utile de l'après-midi. Faites-le en direct dans `/docs`, avec la route `POST /artists`.

## 13.1 Champ obligatoire manquant

```json
{
    "genre": "Alternative",
    "country": "UK"
}
```

Réponse — statut **422** :

```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "name"],
            "msg": "Field required",
            "input": {"genre": "Alternative", "country": "UK"}
        }
    ]
}
```

## 13.2 Mauvais type

```json
{
    "name": "Gorillaz",
    "genre": "Alternative",
    "country": "UK",
    "active": "hello"
}
```

Réponse — **422** :

```json
{
    "detail": [
        {
            "type": "bool_parsing",
            "loc": ["body", "active"],
            "msg": "Input should be a valid boolean, unable to parse string as a boolean",
            "input": "hello"
        }
    ]
}
```

## 13.3 Conversion réussie

```json
{
    "name": "Gorillaz",
    "genre": "Alternative",
    "country": "UK",
    "active": "true"
}
```

Ici pas d'erreur : `"true"` est convertible en booléen. Pydantic est strict sur ce qui est ambigu, tolérant sur ce qui ne l'est pas.

## 13.4 Plusieurs erreurs d'un coup

```json
{
    "active": 42
}
```

`detail` est une **liste** : vous obtenez toutes les erreurs en une seule réponse, pas la première seulement. Pour un développeur front qui consomme votre API, c'est précieux.

## 13.5 Le 422

`422` signifie : « j'ai bien reçu et compris ta requête, mais son contenu ne respecte pas ce que j'attends ». Le JSON était syntaxiquement valide, mais sémantiquement inutilisable.

À distinguer du `400 Bad Request`, plus générique. La spécification HTTP autorise les deux dans ce cas, et le débat existe. Ce qui compte : FastAPI utilise `422` pour toutes les erreurs de validation, et vous n'avez rien à coder pour ça. Le champ `loc` dit toujours où chercher : `["body", "name"]`, `["path", "artist_id"]`, `["query", "limit"]`.

---

# 14. POST /artists

## 14.1 Créer réellement l'artiste

Trois choses à faire : générer un id, construire le dictionnaire, l'ajouter à la liste.

```python
@app.post("/artists")
def create_artist(artist: ArtistCreate):
    if artists:
        new_id = max(existing["id"] for existing in artists) + 1
    else:
        new_id = 1

    new_artist = {"id": new_id, **artist.model_dump()}
    artists.append(new_artist)

    return new_artist
```

## 14.2 Détails

**L'id.** Le client ne l'envoie pas — c'est au serveur de l'attribuer. C'est pour ça que `ArtistCreate` ne contient pas de champ `id` : le modèle décrit ce que le **client** a le droit d'envoyer. Sinon n'importe qui pourrait imposer l'id 1.

`max(...) + 1` sur une liste vide lève une `ValueError`, d'où le `if artists:`. Dans une vraie base de données, c'est le moteur qui gère les identifiants ; ici on bricole, et on l'assume.

**`{"id": new_id, **artist.model_dump()}`** — le `**` déballe le dictionnaire produit par Pydantic dans le nouveau. On obtient un dict avec `id`, `name`, `genre`, `country`, `active`. Version équivalente si le `**` gêne :

```python
    new_artist = artist.model_dump()
    new_artist["id"] = new_id
```

**`artists.append(...)`** — la mutation de la liste globale. C'est ça, notre « écriture en base » pour aujourd'hui.

**Le return.** On renvoie l'artiste créé, avec son id. C'est une convention forte : le client a besoin de connaître l'id pour pouvoir modifier ou supprimer la ressource ensuite.

## 14.3 Le test complet

Entrée :

```json
{
    "name": "Gorillaz",
    "genre": "Alternative",
    "country": "UK"
}
```

Sortie :

```json
{
    "id": 6,
    "name": "Gorillaz",
    "genre": "Alternative",
    "country": "UK",
    "active": true
}
```

`active` apparaît alors qu'on ne l'a pas envoyé : c'est la valeur par défaut du modèle.

Enchaînez avec `GET /artists` : Gorillaz est dans la liste. Vous venez d'écrire un cycle création/lecture complet.

---

# 15. Exercice 3 — POST /albums

**Temps : 25 minutes.**

À vous de rendre la ressource `albums` créable.

## Obligatoire

**1.** Un modèle Pydantic 

**2.** Une route `POST /albums` qui :

- reçoit ce body ;
- génère un nouvel id ;
- ajoute l'album à la liste `albums` ;
- retourne l'album créé, id compris.

## Tests à faire, dans cet ordre

| Test | Attendu |
| --- | --- |
| body valide | l'album créé avec `"id": 9` |
| `GET /albums` ensuite | 9 albums |
| `GET /albums?artist_id=...` | votre album apparaît dans le filtre |
| body sans `title` | 422, avec `loc: ["body", "title"]` |
| `"year": "mille-neuf-cent"` | 422 |
| `"year": "1994"` (chaîne) | ça passe — expliquez pourquoi |
| deux créations successives | ids 9 puis 10 |

Body de test suggéré :

```json
{
    "title": "Recovery",
    "artist_id": 3,
    "year": 2010
}
```

## Bonus

**3.** Vérifiez que `artist_id` correspond bien à un artiste existant. Si ce n'est pas le cas, ne créez pas l'album et renvoyez pour l'instant :

```json
{
    "error": "Artist not found"
}
```

Testez avec `"artist_id": 999`.

On verra la manière HTTP correcte de signaler ça juste après — c'est le sujet de la prochaine démo.

---

# 16. Les limites de la mock data

Petit exercice de trente secondes, à faire tous ensemble.

1. `GET /albums` — votre album créé est bien là, avec l'id 9.
2. Dans le terminal : `Ctrl+C`.
3. Relancez : `fastapi dev main.py`.
4. `GET /albums` à nouveau.

Il a disparu.

```text
Les listes existent uniquement dans la mémoire du processus Python.
```

Quand le processus s'arrête, la mémoire est libérée. Au redémarrage, Python réexécute `main.py` de haut en bas, et `albums = [...]` recrée la liste initiale. Tout ce qui a été ajouté pendant l'exécution est perdu.

Ça vaut aussi pour le rechargement automatique : sauvegardez `main.py` pendant que le serveur tourne, et vos données créées disparaissent également. C'est une source de confusion classique — vous allez le vivre plusieurs fois cet après-midi, maintenant vous savez pourquoi.

> Une vraie application stocke ses données ailleurs que dans la mémoire du processus : dans une base de données.

C'est le sujet d'un des prochains jours. Aujourd'hui, les listes en mémoire sont parfaites : elles nous permettent de nous concentrer sur HTTP, les routes et la validation, sans ajouter la complexité d'une base.

Deuxième limite, plus discrète : si vous lancez plusieurs processus de votre application (ce qu'on fait toujours en production), chacun a **sa propre copie** des listes. Un album créé sur le processus A est invisible depuis le processus B. Une mock data en mémoire ne fonctionne pas au-delà de la machine du développeur.

---

# 17. Codes HTTP essentiels

Le code de statut est la première information que lit un client. Il doit être juste.

```text
200 OK
201 Created
204 No Content

400 Bad Request
404 Not Found
422 Unprocessable Content / erreur de validation

500 Internal Server Error
```

Les familles, pour se repérer : `2xx` ça a marché, `4xx` le client a fait une erreur, `5xx` le serveur a un problème.

Quand utiliser lesquels :

| Code | Situation |
| --- | --- |
| `200 OK` | GET réussi, PATCH ou PUT réussi qui renvoie la ressource |
| `201 Created` | POST qui a créé une ressource |
| `204 No Content` | DELETE réussi, ou toute action réussie sans rien à renvoyer |
| `400 Bad Request` | requête invalide pour une raison métier (ex. : cet artiste existe déjà) |
| `404 Not Found` | la ressource demandée n'existe pas |
| `422` | le body ou un paramètre ne respecte pas les types attendus — FastAPI le fait pour vous |
| `500` | une exception non gérée dans votre code |

Deux confusions classiques à lever tout de suite :

- **`404` ne veut pas dire « l'URL n'existe pas »**, mais « la ressource n'existe pas ». `GET /albums/999` est une route parfaitement valide de votre API ; c'est l'album 999 qui manque.
- **Un `500`, c'est votre faute, pas celle du client.** Si vous en voyez un, allez lire la stack trace dans le terminal.

Il existe une soixantaine de codes standards. Ces sept-là couvrent l'immense majorité des cas d'une API CRUD.

---

# 18. Status codes dans FastAPI

Par défaut, FastAPI répond `200` sur toutes vos routes. Pour un POST qui crée une ressource, c'est imprécis : `201 Created` dit explicitement « quelque chose de nouveau existe maintenant ».

```python
from fastapi import FastAPI, status
```

```python
@app.post("/artists", status_code=status.HTTP_201_CREATED)
def create_artist(artist: ArtistCreate):
    ...
```

On pourrait écrire `status_code=201`. Les constantes de `status` sont préférables : `HTTP_201_CREATED` est auto-documenté, et une faute de frappe devient une erreur d'import au lieu d'un code de statut absurde envoyé en production.

Refaites un POST dans `/docs` : la réponse affiche maintenant `201`. C'est aussi visible dans la documentation de la route, sans commentaire à écrire.

Pourquoi s'embêter ? Parce que le code de statut fait partie du contrat de votre API. Un client bien écrit distingue `200` de `201`, et surtout `200` de `404`. Répondre `200` à tout force chaque consommateur de l'API à deviner en lisant le body — exactement ce qu'on veut éviter.

---

# 19. HTTPException

## 19.1 La bonne façon de renvoyer une erreur

```python
from fastapi import FastAPI, HTTPException, status
```

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Artist not found",
)
```

FastAPI intercepte cette exception et la transforme en réponse HTTP propre :

```json
{
    "detail": "Artist not found"
}
```

avec le bon code de statut cette fois.

## 19.2 `raise`, pas `return`

```python
raise HTTPException(...)   # correct
return HTTPException(...)  # faux
```

`HTTPException` est une **exception**. On la lève. Si vous la retournez, FastAPI reçoit un objet Python quelconque, essaie de le sérialiser en JSON, et vous obtenez un `200` avec un contenu bizarre ou un `500`. C'est une erreur très fréquente, et le symptôme (`200` au lieu de `404`) est déroutant.

Avantage du `raise` : il interrompt la fonction immédiatement. Pas besoin de `else`, pas besoin de gérer le flux après.

## 19.3 On corrige GET /artists/{artist_id}

```python
@app.get("/artists/{artist_id}")
def get_artist(artist_id: int):
    for artist in artists:
        if artist["id"] == artist_id:
            return artist

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Artist not found",
    )
```

Testez `/artists/999` : statut `404`, et un body explicite. Le contrat est maintenant correct — un client peut se fier au code de statut.

## 19.4 Une petite fonction utilitaire

On va avoir besoin de « trouver un artiste par son id, sinon 404 » dans le GET, le PATCH et le DELETE. Trois fois la même boucle, c'est le bon moment pour factoriser :

```python
def find_artist_or_404(artist_id: int) -> dict:
    for artist in artists:
        if artist["id"] == artist_id:
            return artist

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Artist not found",
    )
```

Ce n'est pas une fonction de route : pas de décorateur, c'est une fonction Python normale qu'on appelle depuis les routes.

```python
@app.get("/artists/{artist_id}")
def get_artist(artist_id: int):
    return find_artist_or_404(artist_id)
```

Trois points importants :

- une fonction utilitaire peut parfaitement lever une `HTTPException` — FastAPI l'intercepte quel que soit l'endroit de la pile d'appels ;
- elle renvoie le **dictionnaire de la liste**, pas une copie. Modifier ce dictionnaire modifie bien l'artiste dans `artists`. C'est exactement ce qu'on veut pour le PATCH ;
- on peut aussi l'appeler juste pour son effet de bord — pour vérifier qu'un artiste existe, sans utiliser son retour.

## 19.5 Et pour un refus métier ?

Empêchons la création d'un artiste dont le nom existe déjà :

```python
@app.post("/artists", status_code=status.HTTP_201_CREATED)
def create_artist(artist: ArtistCreate):
    for existing in artists:
        if existing["name"].lower() == artist.name.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artist already exists",
            )
    ...
```

Testez avec `{"name": "Metallica", "genre": "Metal", "country": "US"}` : `400`.

Ici c'est un `400` et pas un `422` : le body est parfaitement valide au niveau des types, c'est la **règle métier** qui refuse. `422` = problème de forme, `400` = problème de logique.

---

# 20. Exercice 4 — Codes HTTP et erreurs sur les Albums

**Temps : 20 minutes.**

Votre API `albums` fonctionne, mais elle ment au client : elle répond `200` même quand ça se passe mal. Corrigez ça.

## Obligatoire

**1.** Écrivez une fonction utilitaire `find_album_or_404(album_id)`, sur le modèle de `find_artist_or_404`. Le `detail` doit être `"Album not found"`.

**2.** Utilisez-la dans `GET /albums/{album_id}`. Plus de `{"error": ...}`.

**3.** `POST /albums` doit répondre `201 Created` en cas de succès.

**4.** Sur `POST /albums`, si `artist_id` ne correspond à aucun artiste, levez une `HTTPException` avec `404` et le detail `"Artist not found"`.

Pour le point 4, réfléchissez avant de coder : vous avez déjà, quelque part dans le fichier, une fonction qui lève exactement ce `404`. Vous pouvez la réutiliser telle quelle.

## Résultats attendus

| Requête | Statut | Body |
| --- | --- | --- |
| `GET /albums/4` | `200` | Meteora |
| `GET /albums/999` | `404` | `{"detail": "Album not found"}` |
| `POST /albums` valide | `201` | l'album créé |
| `POST /albums` avec `artist_id: 999` | `404` | `{"detail": "Artist not found"}` |
| `POST /albums` sans `title` | `422` | erreur de validation |

Vérifiez bien le **code de statut** dans `/docs`, pas seulement le body. C'est tout l'objet de l'exercice.

## Bonus

**5.** Refusez la création d'un album si le même titre existe déjà pour le même artiste. Quel code de statut choisissez-vous, et pourquoi ?

---

# 21. PUT et PATCH

## 21.1 Les deux idées

**PUT** — on remplace la représentation complète de la ressource. Le client envoie l'objet entier tel qu'il doit être après l'opération. Les champs absents sont considérés comme… absents, donc effacés ou remis par défaut.

**PATCH** — on modifie partiellement. Le client envoie seulement les champs à changer. Le reste ne bouge pas.

Exemple parlant. Artiste de départ :

```json
{"id": 1, "name": "Metallica", "genre": "Metal", "country": "US", "active": true}
```

Avec `PATCH /artists/1` et `{"genre": "Thrash Metal"}` : seul le genre change.

Avec `PUT /artists/1` et `{"genre": "Thrash Metal"}` : requête invalide, il manque les autres champs obligatoires. Il faudrait envoyer l'objet complet.

En pratique, PATCH est beaucoup plus utilisé côté API métier : les formulaires d'édition envoient rarement tous les champs, et un PUT partiel écrase silencieusement des données. On se concentre donc sur PATCH.

## 21.2 PUT, pour référence

Puisqu'on remplace tout, on peut réutiliser le modèle de création :

```python
@app.put("/artists/{artist_id}")
def replace_artist(artist_id: int, artist: ArtistCreate):
    existing = find_artist_or_404(artist_id)

    existing.update(artist.model_dump())

    return existing
```

Notez que la fonction a deux paramètres : `artist_id` vient du path (il est entre accolades), `artist` vient du body (c'est un modèle Pydantic). FastAPI fait le tri tout seul, en se basant sur les types. L'`id` n'est pas dans `ArtistCreate`, donc `update()` ne l'écrase pas.

## 21.3 PATCH — le modèle

Pour un PATCH, tous les champs doivent être optionnels :

```python
class ArtistUpdate(BaseModel):
    name: str | None = None
    genre: str | None = None
    country: str | None = None
    active: bool | None = None
```

C'est bien un modèle distinct de `ArtistCreate`. À la création, `name` est obligatoire ; à la modification, ne pas envoyer `name` est légitime. Deux contrats différents, deux modèles.

## 21.4 PATCH — le piège

Naïvement :

```python
update_data = artist_update.model_dump()
# {"name": None, "genre": "Thrash Metal", "country": None, "active": None}
```

Si on applique ça, on écrase `name`, `country` et `active` avec `None`. Le client voulait juste changer le genre, on vient de détruire des données.

Le problème : impossible de distinguer « champ non envoyé » de « champ envoyé à `None` » dans le résultat de `model_dump()`.

Pydantic garde justement la trace de ce qui a été explicitement fourni :

```python
update_data = artist_update.model_dump(exclude_unset=True)
# {"genre": "Thrash Metal"}
```

`exclude_unset=True` retire du dictionnaire tous les champs que le client n'a pas envoyés — les valeurs par défaut ne sont pas incluses. Il ne reste que ce qui a été explicitement fourni. C'est **le** paramètre à connaître pour implémenter un PATCH correct.

## 21.5 PATCH — la route

```python
@app.patch("/artists/{artist_id}")
def update_artist(artist_id: int, artist_update: ArtistUpdate):
    artist = find_artist_or_404(artist_id)

    update_data = artist_update.model_dump(exclude_unset=True)
    artist.update(update_data)

    return artist
```

Cinq lignes de logique. La validation, le 404 et la conversion sont gérés ailleurs.

Rappel utile : `find_artist_or_404` renvoie le dictionnaire présent dans la liste `artists`. `artist.update(...)` modifie donc directement l'élément stocké. Pas besoin de le réinsérer dans la liste.

Test :

```http
PATCH /artists/1
```

```json
{
    "genre": "Thrash Metal"
}
```

Réponse :

```json
{
    "id": 1,
    "name": "Metallica",
    "genre": "Thrash Metal",
    "country": "US",
    "active": true
}
```

Puis un `GET /artists/1` pour confirmer que le changement a bien été conservé.

Deux tests à faire aussi :

- `PATCH /artists/999` : 404 ;
- `PATCH /artists/1` avec un body vide `{}` : rien ne change, `200`. Discutable mais acceptable — c'est une requête valide qui ne demande aucune modification.

---

# 22. DELETE

```python
@app.delete("/artists/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist(artist_id: int):
    artist = find_artist_or_404(artist_id)
    artists.remove(artist)
```

Trois choses.

**Le 404.** Supprimer une ressource inexistante est une erreur du client : on réutilise `find_artist_or_404`.

**`artists.remove(artist)`.** Comme on a le dictionnaire lui-même, `remove()` suffit — pas besoin d'index ni de reconstruire la liste.

**Pas de `return`.** Avec `204 No Content`, on ne renvoie **aucun body**. La fonction ne retourne rien du tout. Si vous essayez de renvoyer un `{"message": "deleted"}` avec un `204`, ça ne passera pas : `204` signifie littéralement « pas de contenu », et le client (comme la spec HTTP) s'attend à un corps vide.

Testez dans `/docs` : la réponse est `204`, sans contenu. Puis `GET /artists` pour vérifier la disparition, et un second `DELETE` sur le même id pour obtenir le `404`.

Alternative parfaitement valable si vous voulez confirmer quelque chose au client :

```python
@app.delete("/artists/{artist_id}")
def delete_artist(artist_id: int):
    artist = find_artist_or_404(artist_id)
    artists.remove(artist)
    return {"deleted": artist_id}
```

Statut `200`, avec un body. Les deux approches existent dans la vraie vie. L'important est de choisir et de rester cohérent dans toute l'API.

**Question à poser à la classe** : on vient de supprimer Metallica. Que sont devenus ses albums ? Ils sont toujours dans la liste `albums`, avec un `artist_id` qui ne pointe plus sur rien. On appelle ça des données orphelines. Trois stratégies possibles :

- supprimer les albums en cascade ;
- refuser la suppression tant qu'il reste des albums (`409 Conflict`) ;
- ne rien supprimer du tout et passer l'artiste à `active: False` — c'est d'ailleurs à ça que sert notre champ `active`, et c'est ce que font la plupart des applications en production.

On y revient dans le challenge final.

À ce stade, `artists` a son CRUD complet : GET collection avec filtres, GET par id, POST, PUT, PATCH, DELETE. C'est une vraie API REST.

---

# 23. Exercice 5 — PATCH et DELETE sur les Albums

**Temps : 20 minutes.**

Dernière pièce du CRUD `albums`.

## Obligatoire

**1.** Un modèle `AlbumUpdate`. C'est à vous de déterminer quels champs il contient et lesquels sont optionnels — relisez la section 21.3 si besoin, mais ne recopiez pas `ArtistUpdate`, les champs d'un album ne sont pas ceux d'un artiste.

**2.** `PATCH /albums/{album_id}` avec `exclude_unset=True`.

**3.** `DELETE /albums/{album_id}` qui renvoie `204` sans body.

Les deux routes doivent renvoyer `404` si l'album n'existe pas.

## Tests

`PATCH /albums/1` avec :

```json
{
    "year": 1985
}
```

Vérifiez que `title` et `artist_id` sont **toujours** présents et inchangés dans la réponse. Si `title` est devenu `null`, vous avez oublié `exclude_unset=True`.

Puis :

| Requête | Statut |
| --- | --- |
| `PATCH /albums/999` | `404` |
| `DELETE /albums/999` | `404` |
| `DELETE /albums/8` | `204`, sans body |
| `DELETE /albums/8` à nouveau | `404` |
| `GET /albums/count` après suppression | `{"count": 7}` |

## Bonus

**4.** Si le client envoie un `artist_id` dans le PATCH, vérifiez que cet artiste existe. Attention : le champ est optionnel, donc il n'est pas toujours dans `update_data`.

---

# 24. Challenge final — Les membres

**Temps : le temps qu'il reste.** Vous ne finirez probablement pas tout, et ce n'est pas grave : la correction est complète et vous pourrez la comparer chez vous.

Vous avez construit `albums` en suivant mes démos, étape par étape. Cette fois, plus de démo : je vous donne une spécification, vous concevez et implémentez.

## Le contexte

Le label veut gérer les **membres** des groupes. Attention : tous les artistes ne sont pas des groupes. Eminem et Adele sont des artistes solo et n'ont pas de membres. Ce n'est pas un problème — leur liste de membres sera simplement vide.

Ajoutez cette mock data :

```python
members = [
    {"id": 1, "artist_id": 1, "name": "James Hetfield", "role": "Vocals"},
    {"id": 2, "artist_id": 1, "name": "Lars Ulrich", "role": "Drums"},
    {"id": 3, "artist_id": 1, "name": "Kirk Hammett", "role": "Guitar"},
    {"id": 4, "artist_id": 1, "name": "Robert Trujillo", "role": "Bass"},
    {"id": 5, "artist_id": 2, "name": "Mike Shinoda", "role": "Vocals"},
    {"id": 6, "artist_id": 2, "name": "Brad Delson", "role": "Guitar"},
    {"id": 7, "artist_id": 2, "name": "Joe Hahn", "role": "Turntables"},
    {"id": 8, "artist_id": 4, "name": "Thomas Bangalter", "role": "Production"},
    {"id": 9, "artist_id": 4, "name": "Guy-Manuel de Homem-Christo", "role": "Production"},
]
```

## Partie obligatoire

**1.** Les modèles `MemberCreate` et `MemberUpdate`. À vous de décider ce qui est obligatoire à la création et optionnel à la modification.

**2.** Le CRUD complet :

```http
GET    /members
GET    /members/{member_id}
POST   /members
PATCH  /members/{member_id}
DELETE /members/{member_id}
```

**3.** Une fonction `find_member_or_404`.

**4.** Les bonnes conventions HTTP, sans que je vous les rappelle route par route :

- `201` à la création ;
- `204` à la suppression ;
- `404` propre partout où c'est nécessaire, avec un `detail` cohérent ;
- vérification que `artist_id` existe à la création d'un membre.

**5.** La route relationnelle :

```http
GET /artists/{artist_id}/members
```

`GET /artists/1/members` renvoie les quatre membres de Metallica. `GET /artists/3/members` renvoie `[]` (Eminem est solo). `GET /artists/999/members` renvoie un `404`.

Réfléchissez à la différence entre les deux derniers cas : liste vide et `404` ne veulent pas dire la même chose.

## Challenge

**6.** La discographie d'un artiste :

```http
GET /artists/{artist_id}/albums
```

**7.** Une route de synthèse :

```http
GET /artists/{artist_id}/summary
```

```json
{
    "artist": {
        "id": 1,
        "name": "Metallica"
    },
    "albums_count": 2,
    "members_count": 4
}
```

## Bonus

**8.** Filtrer les membres par rôle :

```http
GET /members?role=Guitar
```

**9.** Les statistiques du label :

```http
GET /stats
```

```json
{
    "artists": 5,
    "albums": 8,
    "members": 9
}
```

**10.** Le plus difficile — un artiste avec toutes ses relations imbriquées :

```http
GET /artists/{artist_id}/details
```

```json
{
    "id": 1,
    "name": "Metallica",
    "genre": "Metal",
    "country": "US",
    "active": true,
    "albums": [
        {"id": 1, "title": "Master of Puppets", "artist_id": 1, "year": 1986},
        {"id": 2, "title": "The Black Album", "artist_id": 1, "year": 1991}
    ],
    "members": [
        {"id": 1, "artist_id": 1, "name": "James Hetfield", "role": "Vocals"}
    ]
}
```

Attention à ne pas modifier le dictionnaire de l'artiste dans la liste `artists` en construisant cette réponse. Réfléchissez à ce que fait `dict.update()` sur un dictionnaire de la mock data.

**11.** Reprenez `DELETE /artists/{artist_id}` et gérez les orphelins, comme discuté après la démo DELETE. Choisissez une stratégie et assumez-la.

# 25. Récapitulatif

## Ce qu'on a construit

Le chemin complet d'une requête, maintenant que tous les morceaux sont en place :

```text
client (/docs, Postman, fetch)
↓
requête HTTP : méthode + path + query + headers + body
↓
Uvicorn reçoit la requête
↓
FastAPI trouve la route qui correspond (dans l'ordre de déclaration)
↓
validation : path params, query params, body (Pydantic)
↓   \
↓    \-- si invalide : 422, la fonction n'est jamais appelée
↓
votre fonction Python s'exécute
↓
lecture / écriture dans les données
↓   \
↓    \-- HTTPException : 404, 400...
↓
valeur de retour convertie en JSON
↓
réponse HTTP : code de statut + body
↓
client
```

## L'API à la fin de la journée

```text
Music Label API

artists                    (construit en démo)
├── GET /artists           + filtres genre / active / limit
├── GET /artists/{id}
├── POST /artists          201
├── PUT /artists/{id}
├── PATCH /artists/{id}
└── DELETE /artists/{id}   204

albums                     (construit par vous)
├── GET /albums            + filtres artist_id / year / min_year / max_year
├── GET /albums/count
├── GET /albums/search
├── GET /albums/{id}
├── POST /albums           201
├── PATCH /albums/{id}
└── DELETE /albums/{id}    204

members                    (challenge final)
├── GET /members           + filtre role
├── GET /members/{id}
├── POST /members          201
├── PATCH /members/{id}
└── DELETE /members/{id}   204

relations
├── GET /artists/{id}/albums
├── GET /artists/{id}/members
├── GET /artists/{id}/summary
├── GET /artists/{id}/details
└── GET /stats
```

## Le mémo

| Concept | Exemple |
| --- | --- |
| route | `/albums` |
| path parameter | `/albums/3` |
| query parameter | `/albums?min_year=2000` |
| body | le JSON d'un POST |
| modèle Pydantic | `AlbumCreate` |
| modèle de mise à jour | `AlbumUpdate` + `exclude_unset=True` |
| erreur | `raise HTTPException(...)` |
| lecture | `GET` |
| création | `POST` + `201` |
| remplacement | `PUT` |
| modification | `PATCH` |
| suppression | `DELETE` + `204` |
| ordre des routes | segments fixes avant segments variables |
| documentation | `/docs` |

---
