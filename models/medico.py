from controllers.controllerMedico import ControllerMedico


class Medico:
    def __init__(self, nome, cognome, ruolo):
        self.nome = nome
        self.cognome = cognome
        self.ruolo = ruolo
        #self.password = password
        self.controller = ControllerMedico()

    def addDataVisita(self, nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo):
        receipt = self.controller.add_medical_record(nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo)
        return receipt

    def getData(self):
        return
    def accessData(self):
        return

    def prescribeExam(self):
        return

    def prescribeDrug(self):
        return

    def prescribeTherapy(self):
        return
