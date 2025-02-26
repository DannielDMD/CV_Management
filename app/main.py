from fastapi import FastAPI

app = FastAPI(title="Gestión de Candidatos - Backend")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Gestión de Candidatos"}
