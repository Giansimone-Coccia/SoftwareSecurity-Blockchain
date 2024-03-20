
import sys
from controllers.controllerMedico import ControllerMedico

class Medico:
    
    def __init__(self, ruolo):
        self.ruolo = ruolo
        #self.password = password
        self.controller = ControllerMedico()

    def _addDataVisita(self, nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo):
        receipt = self.controller.add_medical_record(nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo)
        return receipt


 
    def menuMedico(self):

        _loop = True

        print("Menù per " + self.ruolo)

        while(_loop):

            print("0. Per uscire dal programma")
            print("1. Per inserire una nuova visita medica")
            print("2. Per visualizzare una visita medica effettuata")
            print("3. Visualizza tutte le visite mediche effettuate")

            scelta = input("Digitare la scelta: ")
            while(scelta != "0" and scelta != "1" and scelta != "2" and scelta != "3"):
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

    def _addNewVisita(self):
        
        nome_paziente = input("Inserisci il nome del paziente: ")
        pressione = input("Inserisci la pressione: ")
        battito = input("Inserisci il battito cardiaco: ")
        glicemia = input("Inserisci la glicemia: ")
        temperatura = input("Inserisci la temperatura: ")
        medicine_input = input("Inserisci i farmaci prescritti (separati da virgola): ")
        medicine = medicine_input.split(',')
        data_ora_visita = input("Inserisci la data: ")
        luogo = input("Inserisci il luogo della visita: ")

        ricevuta = self._addDataVisita(nome_paziente, pressione if pressione!="" else "Pressione non pervenuta",
                                       battito if battito!="" else "Misurazione cardiaca non pervenuta", 
                                        glicemia if glicemia!="" else "Misuarazione glicemica non pervenuta", 
                                        temperatura if temperatura!="" else "Misurazione della temperatura non pervenuta",
                                        medicine if medicine_input!="" else "Nessuna medicina somministrata", 
                                        data_ora_visita, 
                                        luogo)
        
        if(ricevuta.status == 1):
            return True
        else:
            return False

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
