from web3 import Web3
import json

class ControllerMedico:
    def __init__(self, web3_provider, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def add_medical_record(self, nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo):
        # Trasmissione della transazione al contratto
        tx_hash = self.contract.functions.addMedicalRecord(nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo).transact({'from': self.web3.eth.defaultAccount})
        # Attendere la conferma della transazione
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt