import sys


class Paziente():
    def __init__(self, nome, cognome, ruolo, password, email):
        self.nome = nome
        self.cognome = cognome
        self.ruolo = ruolo
        self.password = password
        self.email = email

def registerInfo():
    return

def accessData():
    return


def menuPaziente(self):

    _loop = True

    while(_loop):
        print("0. Per uscire dal programma")
        print("1. Per visionare il referto dell'ultima visita")
        print("2. Per visionare il referto in base all'medico")

        scelta = input("Digitare la scelta: ")
        while(scelta != "0" and scelta != "1" and scelta != "2"):
            scelta = input("Digitare la scelta: ")

    if scelta == "0":
        print("Arrivederci !")
        sys.exit()
    elif scelta == "1":
        pass
    elif scelta == "2":
        pass

    


