from fastapi import FastAPI

from app.adapters.api.images import image_router
from app.adapters.api.ws_faces import ws_router

app = FastAPI(docs_url="/docs")


app.include_router(image_router, prefix="/api")
app.include_router(ws_router)
