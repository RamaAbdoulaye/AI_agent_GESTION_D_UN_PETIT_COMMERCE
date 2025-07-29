from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import sqlite3

from models.client import Client, Utilisateur
from models.vente import Vente
from models.produit import Produit, charger_produits
from helpers.utils import get_openai_api_key, API_HOST, API_PORT, enregistrer_message

client = OpenAI(api_key=get_openai_api_key())

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db_connection():
    conn = sqlite3.connect("data/boutiqueRestaurant.db")
    conn.row_factory = sqlite3.Row
    return conn


def demander_a_gpt(question, context):
    prompt = f"""Tu es un assistant qui répond aux questions sur les produits d'un petit commerce.
Voici les données actuelles :

{context}

Question : {question}
Réponse :"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()


@app.get("/", response_class=HTMLResponse)
async def lire_accueil(request: Request):
    conn = get_db_connection()
    produits = conn.execute("SELECT * FROM Produit").fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "produits": produits
    })


@app.post("/retirer", response_class=HTMLResponse)
async def retirer_stock(request: Request, produit_id: int = Form(...), quantite: int = Form(...)):
    conn = get_db_connection()
    produit = conn.execute(
        "SELECT * FROM Produit WHERE id = ?", (produit_id,)).fetchone()

    if produit:
        if produit["quantite_stock"] >= quantite:
            nouvelle_quantite = produit["quantite_stock"] - quantite
            conn.execute("UPDATE Produit SET quantite_stock = ? WHERE id = ?",
                         (nouvelle_quantite, produit_id))
            conn.commit()
            message = f"{quantite} unité(s) retirée(s) du produit {produit['nom']}"
        else:
            message = f"Stock insuffisant pour le produit {produit['nom']}"
    else:
        message = f"Aucun produit avec ID {produit_id}"

    produits_cursor = conn.execute("SELECT * FROM Produit").fetchall()
    conn.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "produits": produits_cursor,
        "message": message
    })


@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, question: str = Form(...)):
    conn = get_db_connection()
    produits = conn.execute("SELECT nom, description FROM Produit").fetchall()
    conn.close()

    # Création d'un contexte texte à partir des produits
    context = "\n".join([f"{p['nom']} : {p['description']}" for p in produits])

    reponse = demander_a_gpt(question, context)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "produits": produits,
        "message": reponse
    })
