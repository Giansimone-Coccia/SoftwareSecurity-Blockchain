import datetime
import sys
from dotenv import load_dotenv
import web3.eth

from Exceptions.IntegrityCheckError import IntegrityCheckError
from controllers.controllerMedico import ControllerMedico
from controllers.controllerOS import ControllerOS
from controllers.controllerPaziente import ControllerPaziente
from controllers.utilities import Utilities
from database.db import db
from mainView import mainView
from models.medico import Medico
from models.operatoreSanitario import OperatoreSanitario
from models.paziente import Paziente
from session.session import session
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend 
import logging
import os

# Press the green button in the gutter to run the script.

""" Da non usare con wi-fi pubblico (es. università) in quanto il database non consente l'accesso con tale tipo di connessione.
Inoltre, importare mysql per l'utilizzo del DB """
load_dotenv()

if __name__ == '__main__':

    # Re-set blockchain:
    controller = ControllerMedico.get_instance()
    controllerP = ControllerPaziente.get_instance()
    controllerOS = ControllerOS.get_instance()


    # Resetto l'applicazione
    Utilities().startApplication(controller,controllerP,controllerOS)   
        
    istanzaDB = db()
    currentSession = session()

    while (True):
        mV = mainView()
        scelta = int(mV.view())
        if (scelta == 0):
            print("Arrivederci!")
            sys.exit()
        elif(scelta == 1):
            controllerP.registraUtente()
        elif(scelta == 2):
            utentiOttenunti = istanzaDB.ottieniDatiAuth()
            for utente in utentiOttenunti:
                print('Professione: ' + utente['Ruolo'])
                print('Username: ' + utente['Username'])
                print('Password: ' + utente['Password'])
                print('***********************************')

            currentSession.eseguiAccesso()
            print("")

            if currentSession.status == "Medico":
                medico = Medico(currentSession)
                medico.menuMedico()
            
            elif currentSession.status == "OperatoreSanitario":
                os = OperatoreSanitario(currentSession)
                os.menuOS()

            elif currentSession.status == "Paziente":
                paziente = Paziente(currentSession)
                paziente.menuPaziente()
  