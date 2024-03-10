
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

            scelta = input("Digitare la scelta: ")
            while(scelta != "0" and scelta != "1" and scelta != "2"):
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
                nomePaziente, pressione, battito, glicemia, temperatura, farmaci, data, luogo = self._visualizzaVisitaFromNomePaziente()
                print("***********************************")
                print("* Nome paziente: " + nomePaziente )
                print("* Pressione: " + pressione )
                print("* Battito cardiaco: " + battito )
                print("* Glicemia: " + glicemia )
                for farmaco in farmaci:
                    print("*** Farmaco prescritto: " + farmaco)
                print("* Data visita: " + data )
                print("* Luogo visita: " + luogo )
                print("***********************************")

    



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
                                        medicine if medicine_input!="" else "Aa,Bb,Cc", #Nessuna medicina somministrata
                                        data_ora_visita, 
                                        luogo)
        
        if(ricevuta.status == 1):
            return True
        else:
            return False
        
    def _visualizzaVisitaFromNomePaziente(self):

        nomePaziente = input("Inserisci il nome del paziente: ")
        values = self.controller.visualizzaRecordMedicoFromNomePaziente(nomePaziente)
        
        return values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7]
        
        


            
            


