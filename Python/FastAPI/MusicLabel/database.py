from fastapi import HTTPException, status

# Mock Data
# -----------------------------------------------------------------------------
# Deux listes Python normales, rien de spécifique à FastAPI. Elles jouent le
# rôle du stockage : c'est là qu'on lit et qu'on écrit.

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


# Fonctions Utilitaires
# -----------------------------------------------------------------------------
# Ce ne sont PAS des routes : aucun décorateur, ce sont des fonctions Python
# normales qu'on appelle depuis les routes.
#
# Deux choses importantes :
#   - une fonction utilitaire peut parfaitement lever une HTTPException :
#     FastAPI l'intercepte peu importe l'endroit de la pile d'appels ;
#   - elle renvoie le DICTIONNAIRE de la liste, pas une copie. Le modifier
#     modifie donc bien la donnée stockée (ce sera pratique pour le PATCH,
#     et piégeux si on lui ajoute des clés par erreur).

def find_artist_or_404(artist_id: int) -> dict:
    for artist in artists:
        if artist["id"] == artist_id:
            return artist  # trouvé -> on sort immédiatement de la fonction

    # On n'arrive ici que si la boucle est allée au bout sans rien trouver.
    # raise, pas return ! HTTPException est une exception : si on la retourne,
    # FastAPI essaie de la sérialiser en JSON et on obtient un 200 avec un
    # contenu bizarre (ou un 500). Le symptôme est très déroutant.
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Artist not found",
    )

def find_album_or_404(album_id: int) -> dict:
    for album in albums:
        if album["id"] == album_id:
            return album

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Album not found"
    )

def find_member_or_404(member_id : int) -> dict:
    for member in members:
        if member["id"] == member_id:
            return member

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": "Member not found"}
    )
