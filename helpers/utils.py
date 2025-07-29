import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()  # Charge le fichier .env automatiquement

API_HOST = os.getenv("API_HOST", "127.0.0.1")  # valeur par défaut au cas où
API_PORT = int(os.getenv("API_PORT", 8000))
# attention au nom de variable (typo)
STREAMLIT_PORT = int(os.getenv("STREMLIT_PORT", 8501))


def get_db_connection():
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, "..", "data", "boutiqueRestaurant.db")
    connection = sqlite3.connect(db_path)
    return connection


def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "La clé OPENAI_API_KEY n'est pas définie dans le fichier .env")
    return key
