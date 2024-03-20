from web3 import Web3
import json

from deploy import Deploy

import sys
sys.path.append("/Users/lauraferretti/Desktop/SoftwareSecurity-Blockchain/database")
import db

class ControllerMedico:
    def __init__(self):

        deploy = Deploy("Medico.sol")
        self.abi, self.bytecode, self.w3, self.chain_id, self.my_address, self.private_key = deploy.create_contract()

        Medico = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        # Get the latest transaction
        self.nonce = self.w3.eth.get_transaction_count(self.my_address)
        # Submit the transaction that deploys the contract
        transaction = Medico.constructor().build_transaction(
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
        self.medico_contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)

        self.database = db()

    def addVisitaMedica(self, DataOra, CFpaziente, IdMedico, NomePrestazione, Esito, Luogo):

        cursor = self.database.conn.cursor()

        idMedico= self.database.ottieniDatiAuth()[0]['Id']

        select_query = """
            SELECT Id
            FROM Paziente
            WHERE CodiceFiscale = %s
            """

        # Esecuzione dell'istruzione per recuperare l'Id del paziente
        cursor.execute(select_query, (CFpaziente))

        IdPaziente = cursor.fetchone()[0]
        
        nome_tabella = "VisitaMedico"

        insert_query = f"""
        INSERT INTO {nome_tabella} (DataOra, IdPaziente, IdMedico, NomePrestazione, Esito, Luogo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Dati da inserire nella visita medica
        data_visita = (DataOra, IdPaziente, IdMedico, NomePrestazione, Esito, Luogo)

        # Esecuzione dell'istruzione per inserire la visita medica
        cursor.execute(insert_query, data_visita)

        # Commit delle modifiche
        self.database.conn.commit()

        # Chiusura del cursore e della connessione
        cursor.close()
        self.database.conn.close()



    #def add_medical_record(self, nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo):
    def add_medical_record(self, nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo):
        # Trasmissione della transazione al contratto

        greeting_transaction = self.medico_contract.functions.addMedicalRecord(nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo).build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.my_address,
                "nonce": self.nonce + 1,
            }
        )

        signed_greeting_txn = self.w3.eth.account.sign_transaction(
            greeting_transaction, private_key=self.private_key
        )
        tx_greeting_hash = self.w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
        #print(tx_greeting_hash)
        #print("Updating stored Value...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
        self.nonce += 1

        if tx_receipt.status == 1:
            # Transaction successful, retrieve updated values
            updated_values = self.medico_contract.functions.getMedicalRecord(self.my_address, nome_paziente).call()
            #print(f"Updated Stored Values: {updated_values}")
        else:
            print("Transaction failed or reverted")



        """         
        tx_hash = self.medico_contract.functions.addMedicalRecord(nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo).transact({'from': self.web3.eth.defaultAccount})
        # Attendere la conferma della transazione
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash) """
        return tx_receipt

    def visualizzaRecordMedicoFromNomePaziente(self, nome_paziente):
        visita = self.medico_contract.functions.getMedicalRecord(self.my_address, nome_paziente).call()
        new_dict = {"nome_paziente":visita[0], "pressione":visita[1], 
            "battito":visita[2], "glicemia":visita[3], 
            "temperatura":visita[4], "farmaci":visita[5],
            "data":visita[6], "luogo":visita[7]}
        out = [new_dict]
        return out
    
    def visualizzaTuttiRecordMedici(self):
        visite = self.medico_contract.functions.getAllVisiteMediche(self.my_address).call()
        out = []
        for visita in visite:
            new_dict = {"nome_paziente":visita[0], "pressione":visita[1], 
                        "battito":visita[2], "glicemia":visita[3], 
                        "temperatura":visita[4], "farmaci":visita[5],
                        "data":visita[6], "luogo":visita[7]}
            out.append(new_dict)
        return out
        