import logging
from controllers.Exceptions.IntegrityCheckError import IntegrityCheckError
from controllers.utilities import Utilities
from database.db import db
from deploy import Deploy
from interface.Ilog import Ilog


class ControllerOS(Ilog):

    _instance = None
    def __init__(self):

        self.logging = logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        self.valoriHashContratto = []

        self._utente = None
        self._utente_inizializzato = False
        
        self.ut = Utilities()
        deploy = Deploy("OSContract.sol")
        self.abi, self.bytecode, self.w3, self.chain_id, self.my_address, self.private_key = deploy.create_contract()

        OSContract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        #MedicoContract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        # Get the latest transaction
        self.nonce = self.w3.eth.get_transaction_count(self.my_address)
        # Submit the transaction that deploys the contract
        transaction = OSContract.constructor().build_transaction(
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
        self.os_contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)

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
        print(self._utente_inizializzato)
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
    def pazientiAssistiti(self):
        os_cf = self._utente[0]
        #Ottengo la lista di tuple riprese dalla tabella curato in cui CFOperatore è uguale al Cf dell'operatore che ha fatto l'accesso
        return filter(lambda curato: curato[0] == os_cf, self.database.ottieniAssistiti())

    @log_actions
    def datiPazientiCuratiOS(self):
        #Ottengo la lista di dati effettivi dei pazienti curati dal medico che ha fatto l'accesso
        return map(lambda assistito: self.database.ottieniDatiUtente('paziente', assistito[1]), self.pazientiAssistiti())

    @log_actions  
    def modificaDatiCartellaAssistito(self, CFPaziente):
        cartella = self.database.ottieniCartellaFromCF(CFPaziente)
        print(cartella)
        print("Ok")

    @log_actions
    def aggiungiPrestazioneVisita(self, cfPaziente,cfOpSanitario, statoSalute, dataVisita, prestazione, luogoPrestazione):
        """Questo metodo aggiunge una visita al db all'interno della tabella
           visitaOperatore"""
        
        tuplaDaAggiungere=(cfPaziente,cfOpSanitario, statoSalute, dataVisita, prestazione, luogoPrestazione)
            
        try:
            if self.database.addTupla("visitaOperatore", *tuplaDaAggiungere):
                # Se l'aggiunta della tupla ha avuto successo, procedi con le operazioni successive
                # Calcola l'hash dei dati
                hash = self.ut.hash_row(self.database.getVisitaOS(tuplaDaAggiungere))
                
                # Chiamata al contratto medico per memorizzare l'hash
                self.os_contract.functions.storeHashVisita(cfOpSanitario, cfPaziente, hash).transact({'from': self.w3.eth.accounts[0]})
                
                # Ottieni e restituisci le visite mediche del paziente
                visite = self.getRecordVisite(cfPaziente)
                return True
            else:
                # Se l'aggiunta della tupla ha fallito, restituisci False
                return False
        
        except Exception as e:
            print("Errore durante l'aggiunta della visita medica:", e)
            return False
    
    def eliminaPrestazioneVisita(self, visita):
        
        return self.database.eliminaVisitaOS(visita) 
    
    @log_actions
    def getRecordVisite(self, CFPaziente):
        visitePaziente = []
        try:
            pazienti = self.database.ottieniDatiUtente('paziente', CFPaziente)
            IdOS = self.utente[0]
            hash_visite = self.os_contract.functions.retrieveHashVisita(IdOS, CFPaziente).call()
            if pazienti:
                for index, paziente in enumerate(pazienti):
                    print(f"Paziente selezionato: {paziente[1]} {paziente[2]}, {paziente[3]}")
                    visite = self.database.ottieniVisisteOS(paziente[0], IdOS)
                    print(f"Elenco delle visite effettuate per il paziente {paziente[0]}")
                    indice = 0
                    for visita in visite:  
                        integrita_verificata = False
                        print(f"yolo{visita}")
                        for hash_v in hash_visite:
                            if self.ut.check_integrity(hash_v, visita):
                                visitePaziente.append(visita)
                                print(visita)
                                integrita_verificata = True
                                break
                        if not integrita_verificata:
                            raise IntegrityCheckError("Integrità dati: visite non rispettata !")
            else:
                print("Nessun paziente trovato con il codice fiscale specificato.")
        except IntegrityCheckError as e:
            print(f"ERRORE ! {e}")
        except Exception as e:
            print(f"Si è verificato un'errore: {e}")
        return visitePaziente
    
    @log_actions
    def addAssistito(self, CFpaziente):
        IdOperatore = self.utente[0]

        if  not any((assistito[0] == IdOperatore and assistito[1] ==CFpaziente )for assistito in self.database.ottieniAssistiti()):
            return self.database.addTupla("assistito",IdOperatore,CFpaziente)
        else:
            return False
