from database.db import db

class session: 

    def __init__(self,status = None):
        self.status = status
        
        
    def eseguiAccesso(self,email,password):
        istanzaDB = db()

        if(istanzaDB.gestisciAccesso(email,password)):
            self.status = istanzaDB.ottieniProfessione(email,password)
            print("ACCESSO EFFETTUATO !")
        else: 
            print("ACCESSO NEGATO !")

   



            



