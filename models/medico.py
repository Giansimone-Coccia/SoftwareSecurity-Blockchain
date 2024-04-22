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
            print("4. Per aggiornare la Cartella Clinica di un paziente")
            print("5. Per aggiungere un nuovo paziente in cura")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(7))):
                scelta = input("Scelta errata, digitare nuovamente: ")
            print("")

            if(scelta == "0"):
                
                print("Arrividerci !")
                sys.exit()

            elif(scelta == "1"):
                if(self._addNewVisita() == True):
                    print("Visita correttamente salvata nel sistema !")
                    print("")

            elif(scelta == "2"):
                lista = self._selectPaziente()
                if(lista):
                    tupla = lista[0]
                    self.controller.visualizzaRecordVisite(tupla)
            
            elif(scelta == "3"):
                lista = self._selectPaziente()
                if(lista):
                    tupla = lista[0]
                    visita = self._selectVisitaPaziente(tupla)
                    self._modificaVisitaPaziente(visita)

            elif(scelta == "4"):
                cf_paziente = self._selectPaziente()
                    
                if(cf_paziente):
                    cf_paziente=cf_paziente[0]
                    if(self._updateCartellaClinica(cf_paziente) == True):
                        print("Cartella clinica correttamente aggiornata!")
                        print("")
                    else:
                        print("Cartella clinica non aggiornata correttamente")
                        print("")
            
            elif(scelta == "5"):
                if(self._addNewCurato() == True):
                    print("Paziente in cura correttamente salvato nel sistema !")
                    print("")


    @log_actions
    def _selectVisitaPaziente(self, CFPaziente):
        try:
            visite = self.controller.getRecordVisite(CFPaziente)
            if not visite:
                print("Nessuna visita trovata per il paziente specificato.")
                return None
            for contatore, visita in enumerate(visite, start=0):
                print(f"{contatore}.  Dati: {visita[2]}")
                print(f"    Data e ora: {visita[3]}")
                print(f"    Tipo prestazione: {visita[4]}")
                print(f"    Luogo: {visita[5]}")
            counter = len(visite) - 1
            scelta = input("Digitare la scelta: ")
            while True:
                try:
                    scelta = int(scelta)
                    if scelta < 0 or scelta > counter:
                        raise ValueError
                    break
                except ValueError:
                    scelta = input("Scelta errata, digitare nuovamente: ")
            visita_selezionata = visite[scelta]
            return visita_selezionata
        except Exception as e:
            print(f"Si è verificato un errore durante la selezione della visita: {e}")
            return None

    def _modificaVisitaPaziente(self, visita):
        _loop = True
        while(_loop):
            print("0. Per modificare i dati")
            print("1. Per modificare il tipo di prestazione")
            print("2. Per modificare il luogo")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(3))):
                scelta = input("Scelta errata, digitare nuovamente: ")

            if scelta == "0":
                print("")
                nuovi_dati = input("Digita i nuovi dati:")
                self.controller.eliminaVisitaM(visita)
                if self.controller.addVisitaMedica(visita[3],visita[0], visita[4], nuovi_dati, visita[5]):
                    print("Visita aggiornata correttamente.")
                else:
                    print("Visita non aggiornata.")
                _loop = False

            elif scelta == "1":
                print("")
                self.controller.eliminaVisitaM(visita)
                nuova_prestazione = input("Digita la nuova prestazione:")
                if self.controller.addVisitaMedica(visita[3],visita[0], nuova_prestazione, visita[2] , visita[5]):
                    print("Visita aggiornata correttamente.")
                else:
                    print("Visita non aggiornata.")
                _loop = False

            elif scelta == "2":
                print("")
                self.controller.eliminaVisitaM(visita)
                nuovo_luogo = input("Digita il nuovo luogo:")
                if self.controller.addVisitaMedica(visita[3],visita[0], visita[4], visita[2] , nuovo_luogo):
                    print("Visita aggiornata correttamente.")
                else:
                    print("Visita non aggiornata.")
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
        
        cf_paziente = self._selectPaziente()
        if not cf_paziente:
            return False
        else:
            cf_paziente=cf_paziente[0]
        nome_prestazione = input("Inserisci il nome della prestazione offerta: ")
        esito = input("Inserisci l'esito della prestazione: ")
        luogo = input("Inserisci il luogo dove è avvenuta la prestazione: ")
        ricevuta = self.controller.addVisitaMedica(_dataVisita, cf_paziente, nome_prestazione, esito, luogo)
        if (ricevuta==False):
            print("Visita non salvata, prego riprovare")
            print("")
            return False
        return True
    
    @log_actions
    def _addNewCurato(self):
         # Mi ricavo i nuovi assistiti
        _curatiDisponibili = self.controller.pazientiDisponibili()
        # Gestisco il caso in cui non ci sono pazienti disponibili
        if(len(_curatiDisponibili) == 0):
            print("Nessun paziente da curare disponibile")
            return False
        for (i, curatoDisponibile) in enumerate(_curatiDisponibili, 0):
            print(f"{i}. {curatoDisponibile[1]} {curatoDisponibile[2]}, {curatoDisponibile[3]}")

        scelta = input("Inserisci il numero corrispondente al paziente: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > len(_curatiDisponibili)-1:
            scelta = input("Scelta errata, digitare nuovamente: ")

        ricevuta = self.controller.addCurato(_curatiDisponibili[int(scelta)][0])
        
        if(ricevuta == False):
            print("Paziente in cura non salvato, prego riprovare")
            print("")
    
        return ricevuta
    
    @log_actions
    def _selectPaziente(self):
        pazienti_curati = list(self.controller.datiPazientiCurati())
        if(not pazienti_curati):
            print("Non hai alcun paziente in cura")
            print("")
            return False
        print("Seleziona un paziente:")
        for contatore, pazienteCurato in enumerate(pazienti_curati, start=0):
            print(f"{contatore}: {pazienteCurato[0][1]} {pazienteCurato[0][2]}, {pazienteCurato[0][3]}")
        counter = len(pazienti_curati) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        print("")
        paziente_selezionato = pazienti_curati[int(scelta)]
        return paziente_selezionato[0]

    @log_actions
    def _updateClinica(self, paziente):
        print("0. Per modificare le allergie")
        print("1. Per modificare i trattamenti")
        print("2. Per inserire un farmaco")
        print("3. Per modificare un farmaco")
        print("4. Per inserire una patologia")
        print("5. Per modificare le patologie")

        self._verificaPazienteHaveCartella(paziente)

        option = input("Digitare la scelta: ")
        while(option not in map(str, range(6))):
            option = input("Scelta errata, digitare nuovamente: ")

        if(option == "0"):
            print("")
            nuove_allergie = input("Modifica allergie: ")
            
            update = self.controller.updateCartellaClinica(paziente, "Allergie", nuove_allergie)
            return update
        
        elif(option == "1"):
            print("")
            modifica_trattamento = input("Nuovo trattamento: ")
            
            update = self.controller.updateCartellaClinica(paziente, "Trattamento", modifica_trattamento)
            return update

        elif(option == "2"):
            print("")
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
            print("")
            farmaci = self.controller.ottieniFarmacoPaziente(paziente)
            if(len(farmaci)==0):
                print("Nessun farmaco presente")
                return False
            
            print("Seleziona un farmaco:")
            for index, farmaco in enumerate(farmaci):
                print(f"{index}.  Nome: {farmaco[1]}")
                print(f"    Data e ora: {farmaco[2]}")
                print(f"    Dosaggio: {farmaco[3]}")
            da_modificare = input(" Digitare la scelta: ")
            while not da_modificare.isdigit() or not 0 <= int(da_modificare) < len(farmaci):
                da_modificare = input(" Scelta errata, digitare nuovamente: ")
        
            nuovo_dosaggio = input("Inserisci il nuovo dosaggio: ")
            cf_paziente = paziente
            
            insert = self.controller.modificaDoseFarmaco(nuovo_dosaggio, farmaci[int(da_modificare)])
            return insert
            
        
        elif(option == "4"):
            print("")
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
            print("")
            patologie = self.controller.ottieniPatologiePaziente(paziente)
            if(len(patologie) != 0):
                print("Seleziona una patologia:")
                for index, patologia in enumerate(patologie):
                    print(f"{index}.  Nome: {patologia[1]}")
                    print(f"    Data e ora: {patologia[2]}")
                    print(f"    Patologia in corso: {patologia[3]}")
                da_modificare = input("Digitare la scelta: ")

                while not da_modificare.isdigit() or not 0 <= int(da_modificare) < len(patologie):
                    da_modificare = input(" Scelta errata, digitare nuovamente: ")

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
            
                
                insert = self.controller.modificaStatoPatologia(inCorso, patologie[int(da_modificare)])
                return insert
        return

    @log_actions
    def _verificaPazienteHaveCartella(self, CFpaziente):
        """Questo metodo verifica se il paziente selezionato dispone di una 
           cartella clinica, in caso contrario, ne crea una ed aggiorna la blockchain"""
        self.controller.pazienteHaveCartella(CFpaziente)
