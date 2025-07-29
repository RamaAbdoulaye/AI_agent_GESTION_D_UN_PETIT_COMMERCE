import os
import sqlite3

base_dir = os.path.dirname(__file__)  # dossier où est bdd.py
db_path = os.path.join(base_dir, "..", "data", "boutiqueRestaurant.db")


def creer_tables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Produit(
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL,
        prix REAL NOT NULL,
        quantite_stock INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Personne(
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL,
        telephone TEXT,
        email TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Utilisateur(
        id INTEGER PRIMARY KEY,
        FOREIGN KEY(id) REFERENCES Personne(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Client(
        id INTEGER PRIMARY KEY,
        FOREIGN KEY(id) REFERENCES Personne(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Vente(
        id INTEGER PRIMARY KEY,
        quantite INTEGER NOT NULL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        produit_id INTEGER,
        client_id INTEGER,
        FOREIGN KEY(produit_id) REFERENCES Produit(id) ON DELETE CASCADE,
        FOREIGN KEY(client_id) REFERENCES Client(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Plat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        description TEXT,
        prix REAL NOT NULL,
        image TEXT
    );
    """)

    # Afficher les tables existantes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables créées :", tables)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    creer_tables()
