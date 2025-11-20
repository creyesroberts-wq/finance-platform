from fastapi import FastAPI
from backend.routers import corporate, personal

app = FastAPI()

app.include_router(corporate.router, prefix="/corporate", tags=["Corporate"])
app.include_router(personal.router, prefix="/personal", tags=["Personal"])

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
