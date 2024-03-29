
import datetime
import sys
from controllers.controllerMedico import ControllerMedico

class Medico:
    
    def __init__(self, ruolo):
        self.ruolo = ruolo
        #self.password = password
        self.controller = ControllerMedico()

    def _addDataVisita(self, data_ora_vista, cf_paziente, nome_prestazione, esito, luogo):
        receipt = self.controller.addVisitaMedica(data_ora_vista, cf_paziente, nome_prestazione, esito, luogo)
        return receipt

    def _addCurato(self, cf_paziente):
        receipt = self.controller.addCurato(cf_paziente)
        return receipt
        
 
    def menuMedico(self):

        _loop = True

        print("Menù per " + self.ruolo)

        while(_loop):

            print("0. Per uscire dal programma")
            print("1. Per inserire una nuova visita medica")
            print("2. Per visualizzare una visita medica effettuata")
            print("3. Visualizza tutte le visite mediche effettuate")
            print("4. Per aggiungere un nuovo paziente in cura")
            print("5. Per aggiornare la Cartella Clinica di un paziente")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(6))):
                scelta = input("Digitare la scelta: ")
            
            if(scelta == "0"):
                print("Arrividerci !")
                sys.exit()

            elif(scelta == "1"):
                if(self._addNewVisita() == True):
                    print("Visita correttamente salvata nel sistema !")
                    print("")
                else:
                    print("Visita non salvata, prego riprovare")
                    print("")

            elif(scelta == "2"):               
                self._formattaVisita(self._visualizzaVisitaFromNomePaziente())
                
            elif scelta == "3":
                self._formattaVisita(self._visualizzaTutteVisiteMediche())

            elif(scelta == "4"):
                if(self._addNewCurato() == True):
                    print("Paziente in cura correttamente salvato nel sistema !")
                    print("")
                else:
                    print("Paziente in cura non salvato, prego riprovare")
                    print("")
            
            elif(scelta == "5"):
                if(self._updateCartellaClinica(self._selectPaziente()) == True):
                    print("Cartella clinica correttamente aggiornata!")
                    print("")
                else:
                    print("Cartella Clinica non aggiornata, prego riprovare")
                    print("")

    def _addNewVisita(self):

        data_ora_visita = datetime.datetime.now()
        cf_paziente = self._selectPaziente()[0]
        nome_prestazione = input("Inserisci il nome della prestazione offerta: ")
        esito = input("Inserisci l'esito della prestazione: ")
        luogo = input("Inserisci il luogo dove è avvenuta la prestazione: ")

        print(cf_paziente)

        ricevuta = self._addDataVisita(data_ora_visita, cf_paziente, nome_prestazione, esito, luogo)
        
        return True
    
    def _addNewCurato(self):

        cf_paziente = input("Inserisci il codice fiscale del paziente: ")

        ricevuta = self._addCurato(cf_paziente)

        while(ricevuta != True):
            cf_paziente = input("Inserisci il codice fiscale del paziente:")

            ricevuta = self._addCurato(cf_paziente)
        
        return ricevuta
    
    def _selectPaziente(self):
        pazienti_curati = list(self.controller.datiPazientiCurati())

        print("Seleziona un paziente:")

        for contatore, pazienteCurato in enumerate(pazienti_curati, start=0):
            print(pazienteCurato)
            print(f"Premi {contatore} per selezionare il paziente {pazienteCurato[contatore][1]} {pazienteCurato[contatore][2]}")

        counter = len(pazienti_curati) - 1

        scelta = input("Digitare la scelta: ")

        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")

        paziente_selezionato = pazienti_curati[int(scelta)]

        return paziente_selezionato[0]



    def _updateCartellaClinica(self, paziente):

        print("0. Per modificare le allergie")
        print("1. Per modificare i trattamenti")
        print("2. Per modificare i farmaci")
        print("3. Per modificare le patologie")

        scelta = input("Digitare la scelta: ")

        while(scelta not in map(str, range(4))):
            scelta = input("Digitare la scelta: ")

        if(scelta == 0):
            nuove_allergie = input("Modifica allergie: ")
        
        elif(scelta == 1):
            modifica_trattamento = input("Inserisci il nome del trattamento attuale: ")

        elif(scelta == 2):
            return
        
        elif(scelta == 3):
            return
        
        return

    def _visualizzaVisitaFromNomePaziente(self):
        nomePaziente = input("Inserisci il nome del paziente: ")
        return self.controller.visualizzaRecordMedicoFromNomePaziente(nomePaziente)      
        
    def _visualizzaTutteVisiteMediche(self):
        return self.controller.visualizzaTuttiRecordMedici()
 
    def _formattaVisita(self, listVisiteMediche):
        for visita in listVisiteMediche:
            print("***********************************")
            print("* Nome paziente: " + visita["nome_paziente"] )
            print("* Pressione: " + visita["pressione"] )
            print("* Battito cardiaco: " + visita["battito"] )
            print("* Glicemia: " + visita["glicemia"] )
            print("* Temperatura: " + visita["temperatura"] )
            for farmaco in visita["farmaci"]:
                print("*** Farmaco prescritto: " + farmaco)
            print("* Data visita: " + visita["data"] )
            print("* Luogo visita: " + visita["luogo"] )
            print("***********************************")