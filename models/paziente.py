import logging
import sys

from controllers.controllerPaziente import ControllerPaziente
from interface.Ilog import Ilog

class Paziente(Ilog):
    def __init__(self, session):
        self.ruolo = session.status
        self.utente = session.utente
        #self.password = password
        self.controller = ControllerPaziente.get_instance()
        self.controller.utente = self.utente
        self.logging = logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    def log_actions(func):
        """Implementazione di un decorator per il logger"""
        def wrapper(self, *args, **kwargs):
            logging.info(f"{self.__class__.__name__}: Chiamato {func.__name__} , Utente: {self.utente}")
            return func(self, *args, **kwargs)
        return wrapper

    @log_actions
    def registerInfo():
        return

    @log_actions
    def accessData():
        return

    @log_actions
    def menuPaziente(self):
        _loop = True
        print("Menù per " + self.ruolo)
        while(_loop):
            print("0. Per uscire dal programma")
            print("1. Per visualizzare le visite mediche")
            print("2. Per visualizzare le visite fatte da un operatore sanitario")
            print("3. Per visionare la propria cartella clinica")
            print("4. Per visionare i farmaci prescritti")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(5))):
                scelta = input("Scelta errata, digitare nuovamente: ")
            print("")

            if scelta == "0":
                print("Arrivederci !")
                sys.exit()
            elif scelta == "1":
                medico = self._selectMedico()
                if(medico):
                    tupla = medico[0]
                    self._visualizzaVisiteDelPaziente(tupla)
            elif scelta == "2":
                operatoreSanitario = self._selectOperatoreSanitario()
                if(operatoreSanitario):
                    tupla = operatoreSanitario[0]
                    self._visualizzaVisiteDelPazienteOperatore(tupla)
            elif scelta == "3":
               self._visualizzaCartellaClinica()
            elif scelta == "4":
                self._visualizzaFarmaciPrescritti()

    @log_actions
    def _visualizzaVisiteDelPaziente(self, CFMedico):
        self.controller.getVisitePaziente(CFMedico)

    @log_actions
    def _visualizzaVisiteDelPazienteOperatore(self, CFOperatore):
        self.controller.getVisitePazienteOperatore(CFOperatore)

    @log_actions
    def _selectMedico(self):
        medici = list(self.controller.datiMedici())
        if(not medici):
            print("Non hai alcun medico al momento")
            print("")
            return False
        print("Seleziona un medico:")
        for contatore, medico in enumerate(medici, start=0):
            print(f"{contatore}: {medico[contatore][1]} {medico[contatore][2]}, {medico[contatore][3]}")
            contatore += 1
        counter = len(medici) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        print("")
        paziente_selezionato = medici[int(scelta)]
        return paziente_selezionato[0]
    
    @log_actions
    def _selectOperatoreSanitario(self):
        operatori = list(self.controller.datiOperatori())
        if(not operatori):
            print("Non hai alcun operatore sanitario al momento")
            print("")
            return False
        print("Seleziona un operatore:")
        for contatore, operatore in enumerate(operatori, start=0):
            print(f"{contatore}: {operatore[contatore][1]} {operatore[contatore][2]}, {operatore[contatore][3]}")
            contatore += 1
        counter = len(operatori) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        print("")
        operatore_selezionato = operatori[int(scelta)]
        return operatore_selezionato[0]
    
    @log_actions
    def _visualizzaCartellaClinica(self):
        self.controller.getCartellaClinica()

    @log_actions
    def _visualizzaFarmaciPrescritti(self):
        self.controller.getFarmaciPrescritti()
