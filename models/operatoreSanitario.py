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
            print("2. Per visualizzare le visite mediche effettuate")
            print("3. Per modificare una visita inserita")
            print("4. Per aggiungere un paziente come assistito")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(5))):
                scelta = input("Scelta errata, digitare nuovamente: ")

            if scelta == "0":
                print("")
                print("Arrivederci !")
                sys.exit()

            elif scelta == "1":
                print("")
                lista = self._selectPaziente()
                if(lista):
                    _cfPaziente = lista[0]
                    _statoSalute = input("Stato salute del paziente: ")
                    _prestazione = input("Insersci la prestazione effettuata: ")
                    _luogoPrestazione = input("Inserisci il luogo: ")
                    ora_corrente = datetime.datetime.now()

                    _dataVisita = datetime.datetime(
                        ora_corrente.year,
                        ora_corrente.month,
                        ora_corrente.day,
                        ora_corrente.hour,
                        ora_corrente.minute,
                        ora_corrente.second
                    )
                    
                    _cfOpSanitario = self.utente[0]
                    
                    if(self._aggiungiVisita(_cfPaziente,_cfOpSanitario, _statoSalute, _dataVisita, _prestazione, _luogoPrestazione)):
                        print("Prestazione aggiunta correttamente !")
                        print("")
                    else:
                        print("Prestazione NON aggiunta")
                        print("")

            elif scelta == "2":
                print("")
                lista = self._selectPaziente()
                if(lista):
                    tupla = lista[0]
                    self._mostraVisite(tupla)

            elif scelta == "3":
                print("")
                lista = self._selectPaziente()
                if(lista):
                    tupla = lista[0]
                    visita = self._selectVisitaPaziente(tupla)
                    self._modificaVisitaPaziente(visita)

            elif scelta == "4":
                print("")
                if(self._addNewAssistito() == True):
                    print("Paziente correttamente salvato come assistito !")
                    print("")
                else:
                    print("Paziente non salvato, prego riprovare")
                    print("")

    @log_actions
    def _selectPaziente(self):
        pazienti_curati = list(self.controller.datiPazientiCuratiOS())
        if(not pazienti_curati):
            print("Non hai alcun paziente in cura")
            print("")
            return False
        print("Seleziona un paziente:")
        for contatore, pazienteCurato in enumerate(pazienti_curati, start=0):
            print(f"{contatore}: {pazienteCurato[0][1]} {pazienteCurato[0][2]}, {pazienteCurato[0][3]}")
            #print(f"{pazienteCurato}")
        counter = len(pazienti_curati) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        print("")
        paziente_selezionato = pazienti_curati[int(scelta)]
        return paziente_selezionato[0]
    
    @log_actions
    def _aggiungiVisita(self, cfPaziente,cfOpSanitario, statoSalute, dataVisita, prestazione, luogoPrestazione):
        return self.controller.aggiungiPrestazioneVisita(cfPaziente,cfOpSanitario, statoSalute, dataVisita, prestazione, luogoPrestazione)

    @log_actions
    def _mostraVisite(self,CFPaziente):
        visite = self.controller.getRecordVisite(CFPaziente)
        for contatore, visita in enumerate(visite, start=0):
            print(f"{contatore}.  Dati: {visita[2]}")
            print(f"    Data e ora: {visita[3]}")
            print(f"    Tipo prestazione: {visita[4]}")
            print(f"    Luogo: {visita[5]}")
        print("")
    
    @log_actions
    def _selectVisitaPaziente(self, CFPaziente):
        visite = self.controller.getRecordVisite(CFPaziente)
        for contatore, visita in enumerate(visite, start=0):
            print(f"{contatore}.  Dati: {visita[2]}")
            print(f"    Data e ora: {visita[3]}")
            print(f"    Tipo prestazione: {visita[4]}")
            print(f"    Luogo: {visita[5]}")
        counter = len(visite) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        print("")
        visita_selezionata = visite[int(scelta)]
        return visita_selezionata

    def _modificaVisitaPaziente(self, visita):
        _loop = True
        while(_loop):
            print("0. Per modificare i dati")
            print("1. Per modificare il tipo di prestazione")
            print("2. Per modificare il luogo")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(3))):
                scelta = input("Scelta errata, digitare nuovamente: ")
            print("")

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
            print("")


    
    @log_actions
    def _addNewAssistito(self):
        # Mi ricavo i nuovi assistiti
        _assistitiDisponibili = self.controller.pazientiDisponibili()
        
        # Stampa un messaggio se non ci sono pazienti disponibili
        if len(_assistitiDisponibili) == 0:
            print("Non ci sono pazienti disponibili tra cui scegliere.")
            return
        
        for (i, assistitoDisponibile) in enumerate(_assistitiDisponibili, 0):
            print(f"{i}. {assistitoDisponibile[1]} {assistitoDisponibile[2]}, {assistitoDisponibile[3]}")

        scelta = input("Inserisci il numero corrispondente al paziente: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > len(_assistitiDisponibili)-1:
            scelta = input("Scelta errata, digitare nuovamente: ")

        print("")
        ricevuta = self.controller.addAssistito(_assistitiDisponibili[int(scelta)-1][0])
            
        return ricevuta

