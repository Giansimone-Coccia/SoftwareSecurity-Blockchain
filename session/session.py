from database.db import db

class session: 

    def __init__(self,status = None):
        self.status = status
        
        
    def eseguiAccesso(self):
        istanzaDB = db()

        professione = input("Inserisci la professione: ")
        email = input("Inserisci l'email: ")
        password = input("Inserisci la password: ") 

        # TODO : Inserire dei controlli per gesitre le stringhe di input 
        if(istanzaDB.gestisciAccesso(professione,email,password)):
            self.status = professione
            print("ACCESSO EFFETTUATO !")
        else: 
            print("ACCESSO NEGATO !")
        
