import datetime
import sys
from controllers.controllerOS import ControllerOS

class OperatoreSanitario():
    def __init__(self, session):
        self.ruolo = session.status
        self.utente = session.utente
        self.controller = ControllerOS.get_instance()
        self.controller.utente = self.utente 

    #deve inserire solo informazioni sullo stato di salute del paziente
    def registerInfo():
        return
    
    # TODO : Eliminare impostazioni superflue. l'OP può solo visualizzare e al più aggiungere una prestazione
    def menuOS(self):
        _loop = True
        print("Menù per " + self.ruolo)
        while(_loop):
            print("0. Per uscire dal programma")
            print("1. Per modificare alcuni dati della cartella clinica di un paziente")
            print("2. Per inserire una visita presso un paziente")
            print("3. Per modificare una visita inserita")
            print("4. Per aggiungere un paziente come assistito")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(5))):
                scelta = input("Digitare la scelta: ")

            if scelta == "0":
                print("Arrivederci !")
                sys.exit()
            elif scelta == "1":
                lista = self._selectPaziente()
                tupla = lista[0]
                self._modificaDatiCartellaClinicaAssistito(tupla)
            elif scelta == "2":
                lista = self._selectPaziente()
                _cfPaziente = lista[0]
                _statoSalute = input("Stato salute del paziente: ")
                _prestazione = input("Insersci la prestazione effettuata: ")
                _luogoPrestazione = input("Inserisci il luogo: ")
                _dataVisita = datetime.datetime.now()
                _cfOpSanitario = self.utente[0]
                _toAdd = [_cfPaziente,_cfOpSanitario, _statoSalute, _dataVisita, _prestazione, _luogoPrestazione]
                
                if(self._aggiungiVisita(_toAdd)):
                    print("Prestazione aggiunta correttamente !")
                else:
                    print("Prestazione NON aggiunta")
            elif scelta == "3":
                pass
            elif scelta == "4":
                pass

    def _selectPaziente(self):
        pazienti_curati = list(self.controller.datiPazientiCuratiOS())
        print("Seleziona un paziente:")
        for contatore, pazienteCurato in enumerate(pazienti_curati, start=0):
            print(f"{contatore}: {pazienteCurato[contatore-1][1]} {pazienteCurato[contatore-1][2]}, {pazienteCurato[contatore-1][3]}")
            #print(f"{pazienteCurato}")
        counter = len(pazienti_curati) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        paziente_selezionato = pazienti_curati[int(scelta)]
        print(paziente_selezionato)
        return paziente_selezionato[0]

    def _modificaDatiCartellaClinicaAssistito(self,  CFPaziente):
        self.controller.modificaDatiCartellaAssistito(CFPaziente)
    
    def _aggiungiVisita(self, toAdd):
        return self.controller.aggiungiPrestazioneVisita(toAdd)