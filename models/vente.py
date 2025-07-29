from models.produit import Produit
from models.client import Client


class Vente:
    def __init__(self, id: int, produit: Produit, client: Client, quantite: int, date: str):
        self.id = id
        self.produit = produit
        self.client = client
        self.quantite = quantite
        self.date = date

    def en_dictionnaire(self):
        return {
            "id": self.id,
            "produit_id": self.produit.id,
            "client_id": self.client.id,
            "quantite": self.quantite,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return f"Vente #{self.id} - Produit: {self.produit.nom}, Client: {self.client.nom}, Quantité: {self.quantite}, Date: {self.date}"
