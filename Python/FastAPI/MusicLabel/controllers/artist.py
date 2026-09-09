from fastapi import APIRouter, status, HTTPException
from database import *
from models.artist import *

router = APIRouter(
    prefix="/artist",
    tags=["Artist"]
)



@router.get("/get_artist")
def get_artists(
    genre: str | None = None,
    active: bool | None = None,
    limit: int | None = None
):
    # Le pattern : on part de TOUT, et chaque filtre présent réduit le résultat.
    # C'est ce qui permet de combiner les filtres sans écrire un if par
    # combinaison possible.
    result = artists

    # "is not None" et pas "if genre:" !
    # Avec un booléen, "if active:" ignorerait complètement ?active=false,
    # puisque False est falsy en Python. Le bug serait silencieux.
    if genre is not None:
        result = [
            artist_item for artist_item in result
            if artist_item["genre"].lower() == genre.lower()
        ]

    # On filtre sur "result" et pas sur "artists" : c'est ce qui rend les
    # filtres cumulables. En repartant de "artists" ici, le filtre genre
    # serait écrasé.
    if active is not None:
        result = [
            artist_item for artist_item in result
            if artist_item["active"] == active
        ]

    # limit n'est pas un filtre sur le contenu : c'est un paramètre de
    # configuration de la réponse. C'est le tout début de la pagination.
    if limit is not None:
        result = result[:limit]

    # Aucun résultat => liste vide avec un 200. Ce n'est PAS une erreur : la
    # requête était valide, il n'y a simplement rien qui corresponde.
    # Surtout pas de 404 ici.
    return result

    # VERSION 1 — un seul filtre, boucle explicite
    # if genre is None:
    #     return artists

    # new_artist = []

    # for artist_item in artists:
    #     if artist_item["genre"].lower() == genre.lower():
    #         new_artist.append(artist_item)

    # return new_artist

    # VERSION COMPREHENSION LIST (MEME CHOSE)
    # Une liste vide + une boucle + un append conditionnel, ça s'écrit
    # toujours en une compréhension de liste.
    # return [
    #     artist_item for artist_item in artists
    #     if artist_item["genre"].lower() == genre.lower()
    # ]



# Route "de détail" : elle renvoie UN artiste.
#
# Les accolades déclarent un PATH PARAMETER, un segment variable de l'URL.
# Le nom entre accolades ({artist_id}) doit correspondre exactement au nom du
# paramètre de la fonction : c'est comme ça que FastAPI fait le lien.
#
# Le ": int" est le point le plus important du fichier. Dans une URL tout est
# du texte : /artists/1 transporte la chaîne "1". En annotant int, on demande
# à FastAPI de convertir, et de refuser si ce n'est pas convertible :
#
#   /artists/1      -> Metallica
#   /artists/999    -> 404 {"detail": "Artist not found"}
#   /artists/test   -> 422, et la fonction n'est même pas appelée
#
# À retenir : FastAPI utilise énormément les annotations de type Python pour
# convertir, valider, et générer la documentation.
@router.get("/get_artist/{artist_id}")
def get_artist(artist_id: int):
    # Une ligne : toute la logique "je cherche, sinon 404" est dans
    # l'utilitaire. Ici on renvoie simplement ce qu'il trouve, et s'il ne
    # trouve pas, il lève l'exception et cette route s'arrête là.
    return find_artist_or_404(artist_id)

@router.get("/{artist_id}/members")
def get_members_of_artist(artist_id : int):

    # Check if artist exists
    find_artist_or_404(artist_id)

    members_list = [member for member in members if member["artist_id"] == artist_id]

    return members_list


@router.get("/{artist_id}/albums")
def get_discography(artist_id : int):

    artist = find_artist_or_404(artist_id)
    artist_albums = []
    for album in albums:
        if album["artist_id"] == artist_id:
            artist_albums.append(album)
    return artist_albums

@router.get("/{artist_id}/summary")
def get_summary(artist_id : int):

    artist = find_artist_or_404(artist_id)

    summary = {
        "artist":{
            "id":artist["id"],
            "name":artist["name"]
        },
        "albums_count":len([album for album in albums if album["artist_id"] == artist_id]),
        "members_count":len([member for member in members if member["artist_id"] == artist_id]),
    }

    return summary

@router.get("/{artist_id}/details")
def get_artist_details(artist_id : int):
    """
    Return Artist details 
    """
    # Check if exist
    artist = find_artist_or_404(artist_id)

    details = artist

    details["album"] = [album for album in albums if album["artist_id"] == artist_id] 

    details["member"] = [member for member in members if member["artist_id"] == artist_id]
    return details

# POST
"""
status_code=... change le code de statut par défaut de la route.
Sans lui, FastAPI répond 200 ; or une création mérite un 201 Created, qui
dit explicitement "quelque chose de nouveau existe maintenant".
On utilise la constante plutôt que 201 en dur : c'est auto-documenté, et une
faute de frappe devient une erreur d'import au lieu d'un code absurde.


"artist: ArtistCreate" est annoté avec un modèle Pydantic => FastAPI comprend
qu'il s'agit du BODY de la requête, et pas d'un query parameter.
"""
@router.post("/create_artist", status_code=status.HTTP_201_CREATED)
def create_artist(artist: ArtistCreate):
    # Validation MÉTIER (à ne pas confondre avec la validation de forme que
    # Pydantic a déjà faite avant d'entrer dans la fonction).
    # On répond 400 et pas 422 : le JSON était parfaitement valide au niveau
    # des types, c'est la règle métier qui refuse.
    for existing in artists:
        if existing["name"].lower() == artist.name.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artist already exists"
            )

    # Génération de l'id : on prend le plus grand existant + 1.
    # Le "if artists:" est indispensable : max() sur une liste vide lève une
    # ValueError. Bricolage assumé de mock data — dans une vraie base, c'est
    # le moteur qui gère les identifiants.
    if artists:
        new_id = max(existing["id"] for existing in artists) + 1
    else:
        new_id = 1

    # model_dump() transforme l'objet Pydantic en dictionnaire, puisque notre
    # stockage est une liste de dicts. (C'est la syntaxe Pydantic v2 ;
    # beaucoup de tutos utilisent encore .dict(), qui est déprécié.)
    new_artist = artist.model_dump()
    new_artist["id"] = new_id

    # => Autre manière de creer directement l'artist
    # Le ** déballe le dictionnaire dans un nouveau. Différence cosmétique :
    # ici l'id se retrouve en PREMIER dans le JSON de réponse, alors qu'avec la
    # version au-dessus il apparaît en dernier. Aucun impact fonctionnel.
    # new_artist = {"id": new_id, **artist.model_dump()}

    # La mutation de la liste globale : c'est notre "écriture en base" du jour.
    artists.append(new_artist)

    # On renvoie l'artiste créé AVEC son id : convention forte, le client a
    # besoin de cet id pour pouvoir modifier ou supprimer la ressource ensuite.
    return new_artist


# DELETE

@router.delete("/delete_artist", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist(artist_id : int):

    # check
    artist = find_artist_or_404(artist_id)

    # delete members
    members_list = [member for member in members if member["artist_id"] == artist_id]

    for elem in members_list:
        members.remove(elem)
    artists.remove(artist)