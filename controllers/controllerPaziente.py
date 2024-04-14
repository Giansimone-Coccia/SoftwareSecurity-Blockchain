
import logging
from controllers.controllerMedico import ControllerMedico
from controllers.utilities import Utilities
from database.db import db
from deploy import Deploy
from interface.Ilog import Ilog

class ControllerPaziente(Ilog):

    _instance = None
    def __init__(self):

        self.logging = logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


        self.valoriHashContratto = []

        self._utente = None
        self._utente_inizializzato = False
        
        self.ut = Utilities()
        deploy = Deploy("PazienteContract.sol")
        self.abi, self.bytecode, self.w3, self.chain_id, self.my_address, self.private_key = deploy.create_contract()

        PazienteContract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        #MedicoContract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        # Get the latest transaction
        self.nonce = self.w3.eth.get_transaction_count(self.my_address)
        # Submit the transaction that deploys the contract
        transaction = PazienteContract.constructor().build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.my_address,
                "nonce": self.nonce,
            }
        )
        # Sign the transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        #print("Deploying Contract!")
        # Send it!
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        #print("Waiting for transaction to finish...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        #print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

        # Working with deployed Contracts
        self.paziente_contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)

        # Attivo lo smart contract: "Cartella Clinica"
        self.database = db()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls() #super().__new__(cls)
        return cls._instance

    @property
    def utente(self):
        return self._utente

    @utente.setter
    def utente(self, value):
        if not self._utente_inizializzato:
            self._utente = value
            self._utente_inizializzato = True
        else:
            raise Exception("Impossibile modificare l'utente dopo l'inizializzazione.")
    
    def log_actions(func):
        """Implementazione di un decorator per il logger"""
        def wrapper(self, *args, **kwargs):
            logging.info(f"{self.__class__.__name__}: Chiamato {func.__name__} , Utente: {self.utente}")
            return func(self, *args, **kwargs)
        return wrapper

    @log_actions  
    def getVisitePaziente(self, CFMedico):
        try:
            CFPaziente = self.utente[0]
            medici = self.database.ottieniDatiUtente('medico', CFMedico)
            hash_visite = self.paziente_contract.functions.retrieveHashVisita(CFMedico, CFPaziente).call()
            if medici:
                for index, medico in enumerate(medici):
                    print(f"Medico selezionato: {medico[1]} {medico[2]}, {medico[3]}")
                    visite = self.database.ottieniVisiteMedico(CFPaziente, medico[0])
                    print(f"Elenco delle visite effettuate per il medico {medico[0]}")
                    indice = 0
                    integrita_verificata = False
                    for visita in visite:
                        for hash_v in hash_visite:
                            if self.ut.check_integrity(hash_v, visita):
                                print(f"{indice} - Dati: {visita[2]}")
                                print(f"    Data e ora: {visita[3]}")
                                print(f"    Tipo prestazione: {visita[4]}")
                                print(f"    Luogo: {visita[5]}")
                                indice += 1
                                integrita_verificata = True
                    if not integrita_verificata:
                        print("Problemi con il controllo dell'integrità")
            else:
                print("Nessun paziente trovato con il codice fiscale specificato.")
        except Exception as e:
            print(f"Si è verificato un'errore: {e}")

    @log_actions
    def getVisitePazienteOperatore(self, CFOperatore):
        try:
            CFPaziente = self.utente[0]
            operatori = self.database.ottieniDatiUtente('operatoreSanitario', CFOperatore)
            hash_visite = self.paziente_contract.functions.retrieveHashVisita(CFOperatore, CFPaziente).call()
            if operatori:
                for index, operatore in enumerate(operatori):
                    print(f"Medico selezionato: {operatore[1]} {operatore[2]}, {operatore[3]}")
                    visite = self.database.ottieniVisiteMedico(CFPaziente, operatore[0])
                    print(f"Elenco delle visite effettuate per il medico {operatore[0]}")
                    indice = 0
                    integrita_verificata = False
                    for visita in visite:
                        for hash_v in hash_visite:
                            if self.ut.check_integrity(hash_v, visita):
                                print(f"{indice} - Dati: {visita[2]}")
                                print(f"    Data e ora: {visita[3]}")
                                print(f"    Tipo prestazione: {visita[4]}")
                                print(f"    Luogo: {visita[5]}")
                                indice += 1
                                integrita_verificata = True
                    if not integrita_verificata:
                        print("Problemi con il controllo dell'integrità")
            else:
                print("Nessun paziente trovato con il codice fiscale specificato.")
        except Exception as e:
            print(f"Si è verificato un'errore: {e}")
    
    @log_actions
    def mediciPresenti(self):
        paziente_cf = self.utente[0]
        #Ottengo la lista di tuple riprese dalla tabella curato in cui CFPaziente è uguale al Cf del paziente che ha fatto l'accesso
        return filter(lambda curato: curato[1] == paziente_cf, self.database.ottieniCurati())

    @log_actions
    def datiMedici(self):
        #Ottengo la lista di dati effettivi del medico per quel paziente
        return map(lambda medico: self.database.ottieniDatiUtente('medico', medico[0]), self.mediciPresenti())
    
    @log_actions
    def operatoriPresenti(self):
        paziente_cf = self.utente[0]
        #Ottengo la lista di tuple riprese dalla tabella curato in cui CFPaziente è uguale al Cf del paziente che ha fatto l'accesso
        return filter(lambda assistito: assistito[1] == paziente_cf, self.database.ottieniAssistiti())

    @log_actions
    def datiOperatori(self):
        #Ottengo la lista di dati effettivi del medico per quel paziente
        return map(lambda operatoreSanitario: self.database.ottieniDatiUtente('operatoreSanitario', operatoreSanitario[0]), self.operatoriPresenti())
    
    @log_actions
    def getCartellaClinica(self):
        try:
            paziente_cf = self.utente[0]
            cartella = self.database.ottieniCartellaFromCF(paziente_cf)
            hash_cartella = self.paziente_contract.functions.retrieveHashCartellaClinica(paziente_cf).call()
            integrita_verificata = False
            if cartella:
                if self.ut.check_integrity(hash_cartella, cartella):
                    print(f"Trattamenti: {cartella[1]}")
                    print(f"Patologie: {cartella[2]}")
                    integrita_verificata = True
                    if not integrita_verificata:
                        print("Problemi con il controllo dell'integrità")
                else:
                    print("Nessuna cartella clinica trovata con il codice fiscale specificato.")
        except Exception as e:
            print(f"Si è verificato un'errore: {e}")

    @log_actions
    def getFarmaciPrescritti(self):
        try:
            paziente_cf = self.utente[0]
            farmaci = self.database.ottieniFarmaci(paziente_cf)
            hash_farmaci = self.paziente_contract.functions.retrieveHashFarmaco(paziente_cf).call()
            integrita_verificata = False
            contatore = 0
            if farmaci:
                print("Lista dei farmaci prescritti: ")
                for farmaco in farmaci:
                    for hash in hash_farmaci:
                        if self.ut.check_integrity(hash, farmaco):
                            print(f"{contatore} - {farmaco[1]} prescritto il {farmaco[2]}, dosaggio: {farmaco[3]}")
                            integrita_verificata = True
                            contatore += 1
                if not integrita_verificata:
                    print("Problemi con il controllo dell'integrità")
            else:
                print("Nessun farmaco trovato con il codice fiscale specificato.")
        except Exception as e:
            print(f"Si è verificato un'errore: {e}")

    @log_actions
    def registraUtente(self):
        # Controllo sul codice fiscale
        while True:
            cf = input("Inserisci codice fiscale (16 caratteri): ")
            if len(cf) != 16:
                print("Il codice fiscale deve contenere esattamente 16 caratteri.")
            else:
                break
        # Controllo sul nome e cognome
        while True:
            nome = input("Inserisci il nome: ")
            if not nome.isalpha():
                print("Il nome deve contenere solo lettere.")
            else:
                break
        while True:
            cognome = input("Inserisci il cognome: ")
            if not cognome.isalpha():
                print("Il cognome deve contenere solo lettere.")
            else:
                break
        # Controllo sulla residenza (in questo esempio non faccio controlli specifici)
        residenza = input("Inserisci la residenza: ")

        self.database.addNuovoPaziente(cf, nome, cognome, residenza)
