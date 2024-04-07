import datetime

import web3.eth


from controllers.controllerMedico import ControllerMedico
from controllers.utilities import Utilities
from database.db import db
from models.medico import Medico
from session.session import session
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend 

# Press the green button in the gutter to run the script.

""" Da non usare con wi-fi pubblico (es. università) in quanto il database non consente l'accesso con tale tipo di connessione.
Inoltre, importare mysql per l'utilizzo del DB """


if __name__ == '__main__':
    
    # Re-set blockchain:
    #controller = ControllerMedico()
    #ut = Utilities()
    #ut.resetHashBlockchain(controller)
    # Ha l'unico scopo di osservare i dati presenti nel db, va levato alla fine 
    #print(web3.eth.get_transaction('0xfc55eee07abb48ccb60ca7286fc83536edcd1cdaeae92009d2e9e1ce141f3b71'))        
    istanzaDB = db()

    utentiOttenunti = istanzaDB.ottieniDatiAuth()
    for utente in utentiOttenunti:
        print('Professione: ' + utente['Ruolo'])
        print('Email: ' + utente['Username'])
        print('Password: ' + utente['Password'])
        print('***********************************')

        # Inizio la sessione e mpi autentico 

    currentSession = session()
    currentSession.eseguiAccesso()
    print("Status utente: " + currentSession.status)
    print(currentSession.email + " " + currentSession.password)

    if currentSession.status == "Medico":
        medico = Medico(currentSession.status)
        medico.menuMedico()
    
    elif currentSession.status == "OperatoreSanitario":
        pass

    elif currentSession.status == "Paziente":
        pass
  