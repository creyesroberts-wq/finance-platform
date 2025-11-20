from fastapi import FastAPI
from backend.routers import corporate, personal

app = FastAPI(
    title="Finance Platform API",
    description="API para gestionar finanzas corporativas y personales",
    version="1.0.0"
)

# Routers
app.include_router(corporate.router, prefix="/corporate", tags=["Corporate"])
app.include_router(personal.router, prefix="/personal", tags=["Personal"])

# Endpoint raíz
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "API funcionando correctamente",
        "endpoints": {
            "corporate": "/corporate",
            "personal": "/personal"
        }
    }

# Endpoint de prueba para Render
@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "ok"}
