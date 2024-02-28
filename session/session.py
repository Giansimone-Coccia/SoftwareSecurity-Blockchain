import sys
import time
from database.db import db

class session: 

    def __init__(self,status = None):
        self.status = status
        self.email = None
        self.password = None
        
        
    def eseguiAccesso(self):
        istanzaDB = db()
        _contaAccessi = 1
        _isLogin = True

        while(_isLogin):

            email = input("Inserisci email: ")
            password = input("Inserisci la password: ")

            if(istanzaDB.gestisciAccesso(email,password)):
                self.status = istanzaDB.ottieniProfessione(email,password)
                self.email = email
                self.password = password
                print("ACCESSO EFFETTUATO !")
                _isLogin = False
                
            else:
                print("ACCESSO NEGATO !")
                self._controlloAccessi(_contaAccessi)
                _contaAccessi = _contaAccessi + 1
                if(_contaAccessi == 6):
                    _contaAccessi = 0



    def _controlloAccessi(self,tentativi):
        _maxAccessi = 5

        if(tentativi == _maxAccessi):
            print("Hai eseguito troppi tentativi, aspetta 1 minuto")
            for i in range(60, -1, -1):
                #print(f"Tempo rimasto: {i // 60}:{i % 60:02}", end='\r')
                sys.stdout.write(f"\rTempo rimasto: {i // 60}:{i % 60:02}")
                sys.stdout.flush()
                time.sleep(1)
            



   



            



