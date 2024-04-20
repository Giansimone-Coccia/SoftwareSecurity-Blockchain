import logging
import sys
import time

import keyboard
from database.db import db
from interface.Ilog import Ilog

class session(Ilog): 

    def __init__(self,status = None):
        self.status = status
        self.email = None
        self.password = None
        self.utente = None
        self._emailTmp = None
        self._tentativi = self._getMaxiAccessi()
        
    def log_actions(func):
        """Implementazione di un decorator per il logger"""
        def wrapper(self, *args, **kwargs):
            logging.info(f"{self.__class__.__name__}: Chiamato {func.__name__}")
            return func(self, *args, **kwargs)
        return wrapper

    @log_actions 
    def eseguiAccesso(self):
        istanzaDB = db()
        _contaAccessi = 1
        _isLogin = True
        _cinquineSbagliate = 1

        while(_isLogin):

            email = input("Inserisci username: ")
            self._emailTmp = email
            password = input("Inserisci la password: ")

            if istanzaDB.gestisciAccesso(email, password):
                self.status = istanzaDB.ottieniProfessione(email, password)
                self.email = email
                self.password = password
                print("ACCESSO EFFETTUATO !")
                CF = istanzaDB.ottieniCF(email, password)

                if self.status == "Medico":
                    self.utente = istanzaDB.ottieniDatiUtente('medico', CF)[0]
                elif self.status == "OperatoreSanitario":
                    self.utente = istanzaDB.ottieniDatiUtente('operatoreSanitario', CF)[0]
                elif self.status == "Paziente":
                    self.utente = istanzaDB.ottieniDatiUtente('paziente', CF)[0]
                _isLogin = False

            else:
                print("ACCESSO NEGATO !")
                self._controlloAccessi(_contaAccessi, _cinquineSbagliate)
                _contaAccessi = _contaAccessi + 1
                if(_contaAccessi == self._getMaxiAccessi()+1):
                    _contaAccessi = 1 # 0
                    _cinquineSbagliate = _cinquineSbagliate + 1

    @log_actions
    def _controlloAccessi(self,tentativi, cinquineSbagliate):
        _maxAccessi = self._getMaxiAccessi()

        if(tentativi == _maxAccessi):

            # Se sbaglio piu di venti volta di fila(5 cinquine), vado in errore e il programma termina l'esecuzione
            if(cinquineSbagliate == 3):
                print("")
                print("Hai effettuato troppi tentativi")
                logging.warning(f"Utente {self._emailTmp} Ha effettuato il numero massimo di tentativi di inserimento password({int(self._getMaxiAccessi()*cinquineSbagliate)}) ed e' stato disconnesso")
                sys.exit()

            
            print("Hai eseguito troppi tentativi, aspetta: ")
            logging.warning(f"Utente {self._emailTmp} ha eseguito {self._tentativi}")
    
            for i in range(150):
                keyboard.block_key(i)
            for i in range(60*cinquineSbagliate, -1, -1):
                #print(f"Tempo rimasto: {i // 60}:{i % 60:02}", end='\r')
                sys.stdout.write(f"\rTempo rimasto: {i // 60}:{i % 60:02}")
                sys.stdout.flush()
                time.sleep(1)
            print("")
            self._tentativi += tentativi
            for i in range(150):
                keyboard.unblock_key(i)

      

    def _getMaxiAccessi(self): return 5
