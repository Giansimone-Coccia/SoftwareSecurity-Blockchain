import datetime
import sys
import web3.eth

from controllers.Exceptions.IntegrityCheckError import IntegrityCheckError
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

# Press the green button in the gutter to run the script.

""" Da non usare con wi-fi pubblico (es. università) in quanto il database non consente l'accesso con tale tipo di connessione.
Inoltre, importare mysql per l'utilizzo del DB """


if __name__ == '__main__':


    # Re-set blockchain:
    controller = ControllerMedico.get_instance()
    controllerP = ControllerPaziente.get_instance()
    controllerOS = ControllerOS.get_instance()
    ut = Utilities()
    #ut.resetHashBlockchain(controller)
    #ut._resetHashCartellaClinica(controller)
    ut._resetHashFarmaci(controllerP)
    ut._resetHashFarmaciM(controller)
    ut._resetHashPatologie(controller)
    ut._resetHashVisiteMedico(controllerP)
    ut._resetHashVisiteMedicoM(controller)
    ut._resetHashCartellaClinica(controllerP)
    ut._resetHashCartellaClinicaM(controller)
    ut._resetHashVisiteOperatoreO(controllerOS)
    ut._resetHashVisiteOperatore(controllerP)

    #hash_visite = controller.medico_contract.functions.
    # Ha l'unico scopo di osservare i dati presenti nel db, va levato alla fine 
    #print(web3.eth.get_transaction('0xfc55eee07abb48ccb60ca7286fc83536edcd1cdaeae92009d2e9e1ce141f3b71'))        
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
                print('Email: ' + utente['Username'])
                print('Password: ' + utente['Password'])
                print('***********************************')

            currentSession.eseguiAccesso()

            if currentSession.status == "Medico":
                medico = Medico(currentSession)
                medico.menuMedico()
            
            elif currentSession.status == "OperatoreSanitario":
                os = OperatoreSanitario(currentSession)
                os.menuOS()

            elif currentSession.status == "Paziente":
                paziente = Paziente(currentSession)
                paziente.menuPaziente()
  