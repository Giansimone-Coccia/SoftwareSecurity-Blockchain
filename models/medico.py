import datetime
import logging
import sys
from controllers.controllerMedico import ControllerMedico
from interface.Ilog import Ilog

class Medico(Ilog):
    
    def __init__(self, session):
        self.ruolo = session.status
        self.utente = session.utente
        #self.password = password
        self.controller = ControllerMedico.get_instance()
        self.controller.utente = self.utente
        self.logging = logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # Configura il logger
    

    
    def log_actions(func):
        """Implementazione di un decorator per il logger"""
        def wrapper(self, *args, **kwargs):
            logging.info(f"{self.__class__.__name__}: Chiamato {func.__name__} , Operatore: {self.utente}")
            return func(self, *args, **kwargs)
        return wrapper

    @log_actions
    def _addDataVisita(self, data_ora_vista, cf_paziente, nome_prestazione, esito, luogo):
        status = self.controller.addVisitaMedica(data_ora_vista, cf_paziente, nome_prestazione, esito, luogo)
        return status
    
    @log_actions
    def _addCurato(self, cf_paziente):
        receipt = self.controller.addCurato(cf_paziente)
        return receipt
    
    @log_actions
    def menuMedico(self):
        _loop = True
        print("Menù per " + self.ruolo)
        while(_loop):
            print("0. Per uscire dal programma")
            print("1. Per inserire una nuova visita medica")
            print("2. Per visualizzare le visite mediche effettuate")
            print("3. Per aggiornare una visita medica")
            print("4. Per aggiungere un nuovo paziente in cura")
            print("5. Per aggiornare la Cartella Clinica di un paziente")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(7))):
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
                lista = self._selectPaziente()
                tupla = lista[0]
                self.controller.visualizzaRecordVisite(tupla)
            
            elif(scelta == "3"):
                lista = self._selectPaziente()
                tupla = lista[0]
                visita = self._selectVisitaPaziente(tupla)
                self._modificaVisitaPaziente(visita)

            elif(scelta == "4"):
                if(self._addNewCurato() == True):
                    print("Paziente in cura correttamente salvato nel sistema !")
                    print("")
                else:
                    print("Paziente in cura non salvato, prego riprovare")
                    print("")
            
            elif(scelta == "5"):
                if(self._updateCartellaClinica(self._selectPaziente()[0]) == True):
                    print("Cartella clinica correttamente aggiornata!")
                    print("")
                else:
                    print("Cartella clinica non aggiornata correttamente")
                    print("")

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
                self.controller.eliminaVisitaM(visita)
                self.controller.addVisitaMedica(visita[3],visita[0], visita[4], nuovi_dati, visita[5])
                _loop = False
            elif scelta == "1":
                self.controller.eliminaVisitaM(visita)
                nuova_prestazione = input("Digita la nuova prestazione:")
                self.controller.addVisitaMedica(visita[3],visita[0], nuova_prestazione, visita[2] , visita[5])
                _loop = False
            elif scelta == "2":
                self.controller.eliminaVisitaM(visita)
                nuovo_luogo = input("Digita il nuovo luogo:")
                self.controller.addVisitaMedica(visita[3],visita[0], visita[4], visita[2] , nuovo_luogo)
                _loop = False

    @log_actions
    def _addNewVisita(self):
        ora_corrente = datetime.datetime.now()

        _dataVisita = datetime.datetime(
            ora_corrente.year,
            ora_corrente.month,
            ora_corrente.day,
            ora_corrente.hour,
            ora_corrente.minute,
            ora_corrente.second
            )
        
        cf_paziente = self._selectPaziente()[0]
        nome_prestazione = input("Inserisci il nome della prestazione offerta: ")
        esito = input("Inserisci l'esito della prestazione: ")
        luogo = input("Inserisci il luogo dove è avvenuta la prestazione: ")
        print(cf_paziente)
        ricevuta = self.controller.addVisitaMedica(_dataVisita, cf_paziente, nome_prestazione, esito, luogo)
        return True
    
    @log_actions
    def _addNewCurato(self):
        cf_paziente = input("Inserisci il codice fiscale del paziente: ")
        ricevuta = self.controller.addCurato(cf_paziente)
        while(ricevuta != True):
            cf_paziente = input("Inserisci il codice fiscale del paziente:")
            ricevuta = self.controller.addCurato(cf_paziente)
        return ricevuta
    
    @log_actions
    def _selectPaziente(self):
        pazienti_curati = list(self.controller.datiPazientiCurati())
        print("Seleziona un paziente:")
        for contatore, pazienteCurato in enumerate(pazienti_curati, start=0):
            print(f"{contatore}: ")
            print(f"{pazienteCurato}")
        counter = len(pazienti_curati) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        paziente_selezionato = pazienti_curati[int(scelta)]
        return paziente_selezionato[0]

    @log_actions
    def _updateCartellaClinica(self, paziente):
        print("0. Per modificare le allergie")
        print("1. Per modificare i trattamenti")
        print("2. Per inserire un farmaco")
        print("3. Per modificare un farmaco")
        print("4. Per inserire una patologia")
        print("5. Per modificare le patologie")

        self._verificaPazienteHaveCartella(paziente)

        option = input("Digitare la scelta: ")
        print(option)

        while(option not in map(str, range(6))):
            option = input("Digitare la scelta: ")

        if(option == "0"):
            nuove_allergie = input("Modifica allergie: ")
            
            update = self.controller.updateCartellaClinica(paziente, "Allergie", nuove_allergie)
            return update
        
        elif(option == "1"):
            modifica_trattamento = input("Nuovo trattamento: ")
            
            update = self.controller.updateCartellaClinica(paziente, "Trattamento", modifica_trattamento)
            return update

        elif(option == "2"):
            nome_farmaco = input("Inserisci il nome del farmaco che vuoi inserire: ")
            dosaggio = input("Inserisci il dosaggio del farmaco: ")
            ora_corrente = datetime.datetime.now()

            _dataPre = datetime.datetime(
                ora_corrente.year,
                ora_corrente.month,
                ora_corrente.day,
                ora_corrente.hour,
                ora_corrente.minute,
                ora_corrente.second
            )

            cf_paziente = paziente
            insert = self.controller.addFarmaco(cf_paziente, nome_farmaco, _dataPre, dosaggio)
            return insert
        
        elif option == "3":
            farmaci = self.controller.ottieniFarmacoPaziente(paziente)
            if(len(farmaci)==0):
                print("Nessun farmaco presente")
                return False
            for index, farmaco in enumerate(farmaci):
                print(f"{index}: {farmaco}")
            da_modificare = input("Scegli il farmaco da modificare: ")
            nuovo_dosaggio = input("Inserisci il nuovo dosaggio: ")
            cf_paziente = paziente
            try:
                farmaco_da_modificare = farmaci[int(da_modificare)][1]
                print(f"farmaco da modificare {farmaco_da_modificare}")
                insert = self.controller.modificaDoseFarmaco(nuovo_dosaggio, farmaci[int(da_modificare)])
                return insert
            except IndexError:
                print("Indice non valido. Riprova.")
                return False
        
        elif(option == "4"):
            nome_patologia = input("Inserisci il nome della patologia che vuoi inserire: ")
            while True:
                inCorso = input("In corso? (SI/NO): ").strip().upper()
                if inCorso == "SI":
                    inCorso = 1
                    break
                elif inCorso == "NO":
                    inCorso = 0
                    break
                else:
                    print("Risposta non valida. Inserisci 'SI' o 'NO'.")
            ora_corrente = datetime.datetime.now()

            _dataPre = datetime.datetime(
                ora_corrente.year,
                ora_corrente.month,
                ora_corrente.day,
                ora_corrente.hour,
                ora_corrente.minute,
                ora_corrente.second
                )
            cf_paziente = paziente
            
            insert = self.controller.addPatologia(cf_paziente, nome_patologia, _dataPre, inCorso)
            
            return insert
        
        elif(option == "5"):
            patologie = self.controller.ottieniPatologiePaziente(paziente)
            if(len(patologie) != 0):
                for index, patologia in enumerate(patologie):
                    print(f"Seleziona {index} per modificare la patologia: {patologia[1]}")
                da_modificare = input("Scegli la patologia di cui modificare lo stato: ")
                
                while True:
                    inCorso = input("Inserisci il nuovo stato, patologia in corso? (SI/NO):").strip().upper()
                    if inCorso == "SI":
                        inCorso = 1
                        break
                    elif inCorso == "NO":
                        inCorso = 0
                        break
                    else:
                        print("Risposta non valida. Inserisci 'SI' o 'NO'.")
            
                try:
                    patologia_da_modificare = patologie[int(da_modificare)][1]
                    print(f"patologia da modificare {patologia_da_modificare}")
                    insert = self.controller.modificaStatoPatologia(inCorso, patologie[int(da_modificare)])
                    return insert
                except IndexError:
                    print("Indice non valido. Riprova.")
                    return False
            
        
        return

    @log_actions
    def _visualizzaVisitaFromNomePaziente(self, CFP):
        return self.controller.visualizzaRecordVisite(CFP)    

    @log_actions  
    def _visualizzaTutteVisiteMediche(self):
        return self.controller.visualizzaTuttiRecordMedici()
 
    @log_actions
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

    @log_actions
    def _verificaPazienteHaveCartella(self, CFpaziente):
        """Questo metodo verifica se il paziente selezionato dispone di una 
           cartella clinica, in caso contrario, ne crea una ed aggiorna la blockchain"""
        self.controller.pazienteHaveCartella(CFpaziente)
