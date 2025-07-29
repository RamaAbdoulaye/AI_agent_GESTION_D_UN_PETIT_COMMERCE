# client.py

class Personne:
    def __init__(self, id, nom, telephone, email):
        self.id = id
        self.nom = nom
        self.telephone = telephone
        self.email = email


class Client(Personne):
    def __init__(self, id, nom, telephone, email, mot_de_passe):
        super().__init__(id, nom, telephone, email)
        self.mot_de_passe = mot_de_passe

    def se_connecte(self, email_entree, mot_de_passe_entree):
        """
        Méthode simple pour simuler une connexion.
        """
        if self.email == email_entree and self.mot_de_passe == mot_de_passe_entree:
            return True
        else:
            return False


class Utilisateur(Personne):
    def __init__(self, id, nom, telephone, email):
        super().__init__(id, nom, telephone, email)
