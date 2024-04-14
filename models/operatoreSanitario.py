import datetime
import logging
import sys
from controllers.controllerOS import ControllerOS
from interface.Ilog import Ilog

class OperatoreSanitario(Ilog):
    def __init__(self, session):
        self.ruolo = session.status
        self.utente = session.utente
        self.controller = ControllerOS.get_instance()
        self.controller.utente = self.utente
        self.logging = logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def log_actions(func):
        """Implementazione di un decorator per il logger"""
        def wrapper(self, *args, **kwargs):
            logging.info(f"{self.__class__.__name__}: Chiamato {func.__name__} , Utente: {self.utente}")
            return func(self, *args, **kwargs)
        return wrapper
    
    #deve inserire solo informazioni sullo stato di salute del paziente
    @log_actions
    def registerInfo():
        return
    
    @log_actions
    def menuOS(self):
        _loop = True
        print("Menù per " + self.ruolo)
        while(_loop):
            print("0. Per uscire dal programma")
            print("1. Per inserire una visita presso un paziente")
            print("2. Per modificare una visita inserita")
            print("3. Per aggiungere un paziente come assistito")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(4))):
                scelta = input("Digitare la scelta: ")

            if scelta == "0":
                print("Arrivederci !")
                sys.exit()
            elif scelta == "1":
                lista = self._selectPaziente()
                _cfPaziente = lista[0]
                _statoSalute = input("Stato salute del paziente: ")
                _prestazione = input("Insersci la prestazione effettuata: ")
                _luogoPrestazione = input("Inserisci il luogo: ")
                _dataVisita = datetime.datetime.now()
                _cfOpSanitario = self.utente[0]
                
                if(self._aggiungiVisita(_cfPaziente,_cfOpSanitario, _statoSalute, _dataVisita, _prestazione, _luogoPrestazione)):
                    print("Prestazione aggiunta correttamente !")
                else:
                    print("Prestazione NON aggiunta")
            elif scelta == "2":
                lista = self._selectPaziente()
                tupla = lista[0]
                visita = self._selectVisitaPaziente(tupla)
                self._modificaVisitaPaziente(visita)
            elif scelta == "3":
                if(self._addNewAssistito() == True):
                    print("Paziente correttamente salvato come assistito !")
                    print("")
                else:
                    print("Paziente non salvato, prego riprovare")
                    print("")

    @log_actions
    def _selectPaziente(self):
        pazienti_curati = list(self.controller.datiPazientiCuratiOS())
        print("Seleziona un paziente:")
        for contatore, pazienteCurato in enumerate(pazienti_curati, start=0):
            print(f"{contatore}: {pazienteCurato[0][1]} {pazienteCurato[0][2]}, {pazienteCurato[0][3]}")
            #print(f"{pazienteCurato}")
        counter = len(pazienti_curati) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        paziente_selezionato = pazienti_curati[int(scelta)]
        return paziente_selezionato[0]
    
    @log_actions
    def _aggiungiVisita(self, cfPaziente,cfOpSanitario, statoSalute, dataVisita, prestazione, luogoPrestazione):
        return self.controller.aggiungiPrestazioneVisita(cfPaziente,cfOpSanitario, statoSalute, dataVisita, prestazione, luogoPrestazione)

    @log_actions
    def _selectVisitaPaziente(self, CFPaziente):
        visite = self.controller.getRecordVisite(CFPaziente)
        for contatore, visita in enumerate(visite, start=0):
            print(f"{contatore}: {visita[2]} {visita[3]}, {visita[4]} , {visita[5]}")
            #print(f"{pazienteCurato}")
        counter = len(visite) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        visita_selezionata = visite[int(scelta)]
        print(visita_selezionata)
        return visita_selezionata

    def _modificaVisitaPaziente(self, visita):
        _loop = True
        while(_loop):
            print("0. Per modificare i dati")
            print("1. Per modificare il tipo di prestazione")
            print("2. Per modificare il luogo")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(3))):
                scelta = input("Digitare la scelta: ")

            if scelta == "0":
                nuovi_dati = input("Digita i nuovi dati:")
                self.controller.eliminaPrestazioneVisita(visita)
                self.controller.aggiungiPrestazioneVisita(visita[0],visita[1],nuovi_dati, visita[3], visita[4], visita[5])
                _loop = False
            elif scelta == "1":
                self.controller.eliminaPrestazioneVisita(visita)
                nuova_prestazione = input("Digita la nuova prestazione:")
                self.controller.aggiungiPrestazioneVisita(visita[0],visita[1],visita[2], visita[3], nuova_prestazione , visita[5])
                _loop = False
            elif scelta == "2":
                self.controller.eliminaPrestazioneVisita(visita)
                nuovo_luogo = input("Digita il nuovo luogo:")
                self.controller.aggiungiPrestazioneVisita(visita[0],visita[1], visita[2], visita[3],visita[4], nuovo_luogo)
                _loop = False


    
    @log_actions
    def _addNewAssistito(self,):
        cf_paziente = input("Inserisci il codice fiscale dell'assistito: ")
        ricevuta = self.controller.addAssistito(cf_paziente)
        while(ricevuta != True):
            cf_paziente = input("Inserisci il codice fiscale dell'assistito:")
            ricevuta = self.controller.addAssistito(cf_paziente)
        return ricevuta
