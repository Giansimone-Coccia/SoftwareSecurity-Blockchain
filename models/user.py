class User:
    def __init__(self, nome, cognome, email):
        self.nome = nome
        self.cognome = cognome
        self.email = email

    def descrizione(self):
        return f"{self.nome} {self.cognome}, Email: {self.email}"

    def saluta(self):
        return f"Ciao, sono {self.nome}!"
    

