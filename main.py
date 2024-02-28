# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from database.db import db
from session.session import session
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
        
    # Ha l'unico scopo di osservare i dati presenti nel db, va levato alla fine 
    istanzaDB = db()
    utentiOttenunti = istanzaDB.ottieniDati()
    for utente in utentiOttenunti:
        print('Professione: ' + utente['Professione'])
        print('Email: ' + utente['Email'])
        print('Password: ' + utente['Password'])
        print('***********************************')

        # Inizio la sessione e mi autentico 

    currentSession = session()
    currentSession.eseguiAccesso()
    print("Status utente: " + currentSession.status)
    print(currentSession.email + " " + currentSession.password)




