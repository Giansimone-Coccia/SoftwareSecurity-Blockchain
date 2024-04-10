import sys

from controllers.controllerPaziente import ControllerPaziente

class Paziente():
    def __init__(self, ruolo):
        self.ruolo = ruolo
        self.controller = ControllerPaziente.get_instance()

    def registerInfo():
        return

    def accessData():
        return

    def menuPaziente(self):
        _loop = True
        print("Menù per " + self.ruolo)
        while(_loop):
            print("0. Per uscire dal programma")
            print("1. Per visualizzare le visite mediche")
            print("2. Per visionare la propria cartella clinica")
            print("3. Per visionare i farmaci prescritti")

            scelta = input("Digitare la scelta: ")
            while(scelta not in map(str, range(4))):
                scelta = input("Digitare la scelta: ")

            if scelta == "0":
                print("Arrivederci !")
                sys.exit()
            elif scelta == "1":
                #CFP = self.controller.database.ottieniDatiAuth[1]
                medico = self._selectMedico()
                tupla = medico[0]
                self._visualizzaVisiteDelPaziente(tupla)
            elif scelta == "2":
                pass
            elif scelta == "3":
                pass

    def _visualizzaVisiteDelPaziente(self, CFMedico):
        self.controller.getVisitePaziente(CFMedico)

    def _selectMedico(self):
        medici = list(self.controller.datiMedici())
        print("Seleziona un medico:")
        for contatore, medico in enumerate(medici, start=0):
            print(f"{contatore}: {medico[contatore][1]} {medico[contatore][2]}, {medico[contatore][3]}")
            contatore += 1
        counter = len(medici) - 1
        scelta = input("Digitare la scelta: ")
        while not scelta.isdigit() or int(scelta) < 0 or int(scelta) > counter:
            scelta = input("Scelta errata, digitare nuovamente: ")
        paziente_selezionato = medici[int(scelta)]
        print(paziente_selezionato)
        return paziente_selezionato[0]
