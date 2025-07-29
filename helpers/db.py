import sqlite3
import os

# Chemin vers la base de données
db_path = os.path.join(os.path.dirname(__file__), "..",
                       "data", "boutiqueRestaurant.db")


def inserer_produit(nom, prix, quantite):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Produit (nom, prix, quantite_stock)
        VALUES (?, ?, ?)
    """, (nom, prix, quantite))
    conn.commit()
    conn.close()
