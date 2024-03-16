# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import datetime
from controllers.controllerMedico import ControllerMedico
from database.db import db
from models.medico import Medico
from session.session import session
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend 

# Press the green button in the gutter to run the script.

""" Da non usare con wi-fi pubblico (es. università) in quanto il database non consente l'accesso con tale tipo di connessione.
Inoltre, importare mysql per l'utilizzo del DB """


if __name__ == '__main__':
        
    # Ha l'unico scopo di osservare i dati presenti nel db, va levato alla fine 

    istanzaDB = db()
    utentiOttenunti = istanzaDB.ottieniDatiAuth()
    for utente in utentiOttenunti:
        print('Professione: ' + utente['Professione'])
        print('Email: ' + utente['Email'])
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
 

    

