from controllers.utilities import Utilities
from database.db import db
from deploy import Deploy


class ControllerOS:

    _instance = None
    def __init__(self):
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
        if not self._utente_inizializzato:
            self._utente = value
            self._utente_inizializzato = True
        else:
            raise Exception("Impossibile modificare l'utente dopo l'inizializzazione.")
        
    """ def pazientiCurati(self):
        print(f"yoylo {self.utente}")
        medico_cf = self.utente[0]
        #Ottengo la lista di tuple riprese dalla tabella curato in cui CFMedico è uguale al Cf del medico che ha fatto l'accesso
        return filter(lambda curato: curato[0] == medico_cf, self.database.ottieniCurati()) """
        
    def datiPazientiCuratiOS(self):
        #Ottengo la lista di dati effettivi dei pazienti curati dal medico che ha fatto l'accesso
        return map(lambda assistito: self.database.ottieniDatiPaziente(assistito[1]))
        
    def modificaDatiCartellaAssistito(self, CFPaziente):
        cartella = self.database.ottieniCartellaFromCF(CFPaziente)
        print("Ok")

    