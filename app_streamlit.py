import streamlit as st
import sqlite3
import openai
import os
from PIL import Image
from helpers.utils import get_openai_api_key
from models.produit import charger_produits
from helpers.db import inserer_produit

# Clé API OpenAI
openai.api_key = get_openai_api_key()

# Créer le dossier pour stocker les images (si non existant)
os.makedirs("images", exist_ok=True)

# Connexion à la base de données (une seule base cohérente !)
conn = sqlite3.connect("data/boutiqueRestaurant.db", check_same_thread=False)
cursor = conn.cursor()

# Menu latéral
st.sidebar.title("Assistant Boutique")
section = st.sidebar.selectbox(
    "Navigation", ["Accueil", "Clients", "Produits",
                   "Ventes", "Statistiques", "Plats"]
)


def demander_a_gpt(question, context):
    prompt = f"""
Tu es un assistant spécialisé pour répondre uniquement aux questions concernant les plats disponibles dans un petit commerce. Tu dois uniquement utiliser les informations listées ci-dessous. Ne donne pas d'informations qui ne sont pas dans cette liste.

Voici la liste des plats disponibles, avec leur description et prix :

{context}

Question : {question}

Réponse précise et courte :
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=300
    )

    return response.choices[0].message["content"].strip()


# -----------------------
# Pages de l'application
# -----------------------
if section == "Accueil":
    st.title("Bienvenue 🎉")
    st.write("Assistant pour la gestion d’un petit commerce.")
    # --- Affichage des plats ---
    cursor.execute("SELECT * FROM Plat")
    plats = cursor.fetchall()

    st.subheader("🍛 Plats disponibles")
    for plat in plats:
        col1, col2 = st.columns([1, 3])
        with col1:
            if plat[4]:  # colonne image
                st.image(plat[4], width=100)
            else:
                st.image("https://via.placeholder.com/100", width=100)
        with col2:
            st.write(f"**{plat[1]}** — {plat[2]} — 💵 {plat[3]} $")

    st.markdown("---")

    # --- Chatbox simple ---
    st.subheader("💬 Posez votre question à l'assistant")

    # Champ pour la question
    question = st.text_input("Votre question")

    # Bouton envoyer
    if st.button("Envoyer"):
        if question:
            # Charger le contexte (produits par ex.) pour la requête GPT
            cursor.execute("SELECT * FROM Produit")
            produits = cursor.fetchall()
            context = ""
            for plat in plats:  # plats est la liste des plats depuis ta DB
                context += f"- {plat[1]} : {plat[2]} (Prix : {plat[3]} $)\n"

            # Appeler GPT avec la question + contexte
            reponse = demander_a_gpt(question, contexte)

            # Afficher la réponse
            st.markdown(f"**Réponse :** {reponse}")
        else:
            st.warning("Veuillez entrer une question.")


elif section == "Clients":
    st.title("👥 Liste des clients")
    cursor.execute("SELECT * FROM Client")
    clients = cursor.fetchall()
    for client in clients:
        st.write(f"🧑 {client[1]} - {client[2]}")

elif section == "Produits":
    st.title("📦 Produits en stock")
    cursor.execute("SELECT * FROM Produit")
    produits = cursor.fetchall()
    for prod in produits:
        st.write(f"{prod[1]} - Stock : {prod[2]} - Prix : {prod[3]} $")

elif section == "Ventes":
    st.title("💰 Historique des ventes")
    cursor.execute("SELECT * FROM Vente")
    ventes = cursor.fetchall()
    for v in ventes:
        st.write(f"Vente ID {v[0]} - Produit ID {v[1]} - Quantité : {v[2]}")

elif section == "Statistiques":
    st.title("📊 Statistiques générales")
    cursor.execute("SELECT COUNT(*) FROM Client")
    st.metric("Nombre de clients", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM Vente")
    st.metric("Nombre de ventes", cursor.fetchone()[0])

elif section == "Plats":
    st.title("🍽️ Gestion des plats")

    # Formulaire d'ajout de plat
    with st.form("ajout_plat"):
        nom = st.text_input("Nom du plat")
        description = st.text_area("Description")
        prix = st.number_input("Prix", min_value=0.0, step=0.5)
        image_file = st.file_uploader(
            "Image du plat", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Ajouter le plat")

        if submit:
            if nom and prix:
                image_path = None
                if image_file:
                    # Enregistre l'image dans le dossier images/
                    image_path = f"images/{nom.replace(' ', '_')}.png"
                    with open(image_path, "wb") as f:
                        f.write(image_file.read())

                # Insertion dans la base de données
                cursor.execute(
                    "INSERT INTO Plat (nom, description, prix, image) VALUES (?, ?, ?, ?)",
                    (nom, description, prix, image_path)
                )
                conn.commit()
                st.success("✅ Plat ajouté avec succès.")
            else:
                st.error("❌ Le nom et le prix sont obligatoires.")

    # Liste des plats
    st.markdown("---")
    st.subheader("🍛 Liste des plats enregistrés")
    cursor.execute("SELECT * FROM Plat")
    plats = cursor.fetchall()

    for plat in plats:
        col1, col2 = st.columns([1, 3])
        with col1:
            if plat[4]:  # index 4 pour la colonne image
                st.image(plat[4], width=100)
            else:
                st.image("https://via.placeholder.com/100", width=100)
        with col2:
            st.write(f"**{plat[1]}** — {plat[2]} — 💵 {plat[3]} $")
