from pydantic import BaseModel
# Model Pydantic
# -----------------------------------------------------------------------------
# Un modèle décrit la FORME des données qu'on attend dans le body d'une requête.
# En héritant de BaseModel, la classe récupère toute la machinerie de Pydantic :
# on n'écrit que la description, la validation est offerte.
#
# Pas de champ "id" dans ces modèles : le modèle décrit ce que le CLIENT a le
# droit d'envoyer. L'id est attribué par le serveur, sinon n'importe qui
# pourrait imposer l'id 1 et écraser une ressource existante.


class AlbumCreate(BaseModel):
    title: str
    artist_id: int
    year: int

class AlbumUpdate(BaseModel):
    title: str | None = None
    artist_id: int | None = None
    year: int | None = None
