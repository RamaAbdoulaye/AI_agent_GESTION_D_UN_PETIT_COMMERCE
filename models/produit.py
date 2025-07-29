from helpers.utils import get_db_connection


class Produit:
    def __init__(self, id, nom, prix, quantite_stock):
        self.id = id
        self.nom = nom
        self.prix = prix
        self.quantite_stock = quantite_stock

    def metre_a_jour_stock(self, quantite):
        self.quantite_stock += quantite

    def retirer_du_stock(self, quantite):
        if quantite > self.quantite_stock:
            print("Stock insuffisant")
            return False
        else:
            self.quantite_stock -= quantite
            return True

    def en_dictionnaire(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "quantite_stock": self.quantite_stock
        }

    def sauvegarder(self):
        conn = get_db_connection()
        conn.execute(
            "UPDATE Produit SET quantite_stock = ? WHERE id = ?",
            (self.quantite_stock, self.id)
        )
        conn.commit()
        conn.close()

    def __str__(self):
        return f"[Produit] {self.nom} | Prix: {self.prix:.2f} | Stock: {self.quantite_stock}"

# Fonction en dehors de la classe pour charger tous les produits


def charger_produits():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Produit").fetchall()
    conn.close()
    return [Produit(row["id"], row["nom"], row["prix"], row["quantite_stock"]) for row in rows]
