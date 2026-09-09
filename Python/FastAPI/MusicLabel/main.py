"""
Music Label API 

Lancement :
    fastapi dev main.py

Adresses utiles :
    http://127.0.0.1:8000/docs          -> Swagger, pour tester les routes
    http://127.0.0.1:8000/openapi.json  -> la description OpenAPI générée seule
"""

from fastapi import FastAPI
from controllers import artist, album, member
from database import *
import uvicorn
# L'application. Un seul objet FastAPI pour tout le projet, "app" par convention.
# C'est lui qui enregistre les routes déclarées plus bas via les décorateurs.
app = FastAPI(
    title="Music Label API",
    version="1.0"
    
)
app.include_router(artist.router)
app.include_router(album.router)
app.include_router(member.router)

@app.get("/stats")
def get_label_stats():
    stats = {
        "artists" : len(artists),
        "albums" : len(albums),
        "members": len(members)
    }

    return stats


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

