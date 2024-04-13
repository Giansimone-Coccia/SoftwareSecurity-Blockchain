class mainView:
    def __init__(self):
        pass

    def view(self):
        print("Benvenuto!")
        print("0. Per uscire dal programma")
        print("1. Per registrarti come paziente")
        print("2. per eseguire l'accesso come utente già registrato")
        scelta = input("Digitare la scelta: ")
        while(scelta not in map(str, range(4))):
            scelta = input("Digitare la scelta: ")
        return scelta