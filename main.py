from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
import uuid
from datetime import datetime

app = FastAPI(title="API Banque")

#Modèles
class CompteCreate(BaseModel):
    nom: str
    email: EmailStr
    code: str
    solde_initial: float = 0.0

class Compte(BaseModel):
    id: str
    nom: str
    email: EmailStr
    solde: float
    date_creation: str

#"Base de données"
comptes_db: List[Compte] = []

#créer un compte
@app.post("/comptes/", response_model=Compte)
def creer_compte(compte: CompteCreate):

    # Vérifier email unique
    for c in comptes_db:
        if c.email == compte.email:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")

    nouveau = Compte(
        id=str(uuid.uuid4())[:8],
        nom=compte.nom,
        email=compte.email,
        solde=compte.solde_initial,
        date_creation=str(datetime.now())
    )

    comptes_db.append(nouveau)
    return nouveau

#liste des comptes
@app.get("/comptes/", response_model=List[Compte])
def lister_comptes():
    return comptes_db