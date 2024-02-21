# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from database.db import db
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    istanzaDB = db()
    utentiOttenunti = istanzaDB.ottieniDati()

    for utente in utentiOttenunti:
        print(utente['Professione'])
        print(utente['Email'])
        print(utente['Password'])