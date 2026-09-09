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



class MemberCreate(BaseModel):
    artist_id : int
    name : str 
    role : str

class MemberUpdate(BaseModel):
    artist_id : int | None = None
    name : str | None = None
    role : str | None = None