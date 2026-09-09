from fastapi import APIRouter, HTTPException, status
from models.album import *
from database import *

router = APIRouter(
    prefix="/albums",
    tags=["Album"]
)



# ALBUMS

# GET

# Même pattern que /artists, avec des filtres propres aux albums.
#
#   GET /albums?artist_id=1
#   GET /albums?year=2003
#   GET /albums?min_year=2000
#   GET /albums?max_year=2 010
#   GET /albums?artist_id=1&min_year=1990     <- les filtres se combinent
#   GET /albums?sort=year
@router.get("/get_albums")
def get_albums(
    artist_id: int | None = None,
    year: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    sort: str | None = None
):
    result = albums

    if artist_id is not None:
        result = [
            album_item for album_item in result 
            if album_item["artist_id"] == artist_id
        ]

    # year = égalité stricte...
    if year is not None:
        result = [
            album_item for album_item in result
            if album_item["year"] == year
        ]

    # ... alors que min_year et max_year sont des COMPARAISONS.
    # Piège classique : inverser >= et <=. Le test avec les deux filtres
    # combinés (?min_year=2000&max_year=2005) le révèle immédiatement.
    if min_year is not None:
        result = [
            album_item for album_item in result
            if album_item["year"] >= min_year
        ]

    if max_year is not None:
        result = [
            album_item for album_item in result
            if album_item["year"] <= max_year
        ]

    # sort n'est pas un filtre : il ne retire rien, il réordonne.
    # sorted() renvoie une NOUVELLE liste (contrairement à .sort() qui
    # modifierait la mock data sur place, ce qu'on ne veut surtout pas ici).
    # key= dit sur quoi comparer : ici l'année de chaque dictionnaire.
    if sort == 'year':
        result = sorted(result, key=lambda album: album["year"])

    return result

# ATTENTION À L'ORDRE DES ROUTES — c'est le piège de l'exercice 2.
#
# FastAPI teste les routes dans l'ordre où elles sont déclarées et s'arrête à
# la première qui correspond. Si /albums/{album_id} était déclarée avant, la
# requête GET /albums/count matcherait /albums/{album_id} avec
# album_id = "count", la conversion en int échouerait, et on obtiendrait un
# 422 sans jamais atteindre cette fonction.
#
# Règle : les segments FIXES (/albums/count, /albums/search) se déclarent
# AVANT les segments VARIABLES (/albums/{album_id}).
@router.get("/count")
def count_albums():
    return {"count": len(albums)}

@router.get("/search")
def search_album(title: str):
    # "title: str" SANS valeur par défaut => paramètre OBLIGATOIRE.
    # GET /albums/search sans ?title= renvoie donc un 422, ce qui est logique :
    # une recherche sans terme de recherche n'a pas de sens.
    result = albums

    # "in" sur une chaîne teste la sous-chaîne, pas le mot entier.
    # Conséquence à connaître : ?title=the remonte aussi "Hybrid Theory",
    # parce que "the" est contenu dans "theory". Ce n'est pas un bug.
    result = [
        album for album in result
        if title.lower() in album["title"].lower()
    ]

    return result

    # Version condensée, strictement équivalente (code mort, gardé en
    # référence) : quand on n'a qu'un seul filtre, la variable intermédiaire
    # n'apporte rien.
    # return [
    #     album for album in albums
    #     if title.lower() in album["title"].lower()
    # ]

# Déclarée en DERNIER parmi les routes /albums/... : segment variable, donc
# après les segments fixes (voir le commentaire au-dessus de /albums/count).
@router.get("/get_album/{album_id}")
def get_album(album_id: int):
    return find_album_or_404(album_id)






# POST
@router.post("/create_album", status_code=status.HTTP_201_CREATED)
def create_album(album: AlbumCreate):
    # Appel de l'utilitaire SANS utiliser son retour : on ne veut pas
    # l'artiste, on veut juste savoir s'il existe. S'il n'existe pas, la
    # fonction lève l'exception et la route s'arrête ici avec un
    # 404 "Artist not found". Une ligne, et le message reste cohérent avec le
    # reste de l'API — c'est tout l'intérêt d'avoir factorisé cet utilitaire.
    find_artist_or_404(album.artist_id)

    # Contrôle métier : pas deux fois le même titre POUR LE MÊME artiste.
    for existing in albums:
        if existing["title"].lower() == album.title.lower() and existing["artist_id"] == album.artist_id:
            # 409 Conflict : plus précis que 400 ici, il dit "ta requête entre
            # en conflit avec l'état actuel de la ressource". 400 se défendrait
            # aussi. Ce qui compte, c'est de ne pas répondre 422, qui est
            # réservé aux erreurs de forme détectées par Pydantic.
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Album already exists for this artist"
            )

    if albums:
        new_id = max(existing["id"] for existing in albums) + 1
    else:
        new_id = 1

    new_album = album.model_dump()
    new_album["id"] = new_id

    albums.append(new_album)

    return new_album

# PUT
@router.put("/replace_album/{album_id}")
def replace_album(album_id: int, album_data: AlbumUpdate):
    """
    Remplace completement l'album existant
    """
    album = find_album_or_404(album_id)
    find_artist_or_404(album_data.artist_id)


    for a in albums:
        if (
            a["artist_id"] == album_data.artist_id 
            and a["title"].lower() == album_data.title.lower()
            and a["id"] != album_id
            ):

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail = f"An album titled '{album_data.title}' already exists for this artist"
            )
    # on remplace toutes les valeurs de l'album
        album["title"] = album_data.title
        album["artist_id"] = album_data.artist_id
        album["year"] = album_data.year
        
        return album



# PATCH
@router.patch("/update_album/{album_id}")
def update_album(album_id: int, album_update: AlbumUpdate, artist_id : int | None = None):
    "Update les champs spécifiés d'un album"
    album_to_modify = find_album_or_404(album_id)

    if artist_id is not None:
        find_artist_or_404(artist_id)
    
    update_data = album_update.model_dump(exclude_unset=True)

    album_to_modify.update(update_data)


# Delete
@router.delete("/delete_album/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(album_id: int):
    """
    Supprime un album sur son id, return 204 
    """
    album_to_delete = find_album_or_404(album_id)

    albums.remove(album_to_delete)
