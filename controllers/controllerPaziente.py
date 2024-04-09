
from controllers.utilities import Utilities
from database.db import db
from deploy import Deploy

class ControllerPaziente:

    _instance = None
    def __init__(self):

        self.valoriHashContratto = []
        
        self.ut = Utilities()
        deploy = Deploy("PazienteContract.sol")
        self.abi, self.bytecode, self.w3, self.chain_id, self.my_address, self.private_key = deploy.create_contract()

        PazienteContract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
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
        #self.cartella_clinica = self._deploy_cartella_clinica("CartellaClinica")
        self.database = db()
        #self.ut.resetHashBlockchain(self)
        #self.utilities = utilities.Utilities()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls() #super().__new__(cls)
        return cls._instance

    def getVisitePaziente(self, CFMedico):
        try:
            CFPaziente = self.database.ottieniDatiAuth()[0]['CF']
            medici = self.database.ottieniDatiMedico(CFMedico)
            #hash_visite = self.medico_contract.functions.retrieveHashVisita(IdMedico, CFPaziente).call()
            if medici:
                for index, medico in enumerate(medici):
                    print(f"Medico selezionato: {medico[1]} {medico[2]}, {medico[3]}")
                    visite = self.database.ottieniVisitePaziente(medico[0], CFPaziente)
                    print(f"Elenco delle visite effettuate per il medico {medico[0]}")
                    indice = 0
                    integrita_verificata = False
                    for visita in visite:
                        #for hash_v in hash_visite:
                            #if self.ut.check_integrity(hash_v, visita):
                        print(f"{indice} - Dati: {visita[2]}")
                        print(f"    Data e ora: {visita[3]}")
                        print(f"    Tipo prestazione: {visita[4]}")
                        print(f"    Luogo: {visita[5]}")
                        indice += 1
                        integrita_verificata = True
                        break
                    if not integrita_verificata:
                        print("Problemi con il controllo dell'integrità")
            else:
                print("Nessun paziente trovato con il codice fiscale specificato.")
        except Exception as e:
            print(f"Si è verificato un'errore: {e}")
    
    def mediciPresenti(self):
        paziente_cf = self.database.ottieniDatiAuth()[0]['CF']
        #Ottengo la lista di tuple riprese dalla tabella curato in cui CFPaziente è uguale al Cf del paziente che ha fatto l'accesso
        return filter(lambda curato: curato[0] == paziente_cf, self.database.ottieniCurati())

    def datiMedici(self):
        #Ottengo la lista di dati effettivi del medico per quel paziente
        return map(lambda medico: self.database.ottieniDatiMedico(medico[1]), self.mediciPresenti())