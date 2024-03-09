from web3 import Web3
import json

from deploy import Deploy

class ControllerMedico:
    def __init__(self):

        deploy = Deploy("/Users/lauraferretti/Desktop/SoftwareSecurity-Blockchain/solidityContracts/Medico.sol")

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
        print("Deploying Contract!")
        # Send it!
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

        # Working with deployed Contracts
        self.medico_contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)

    #def add_medical_record(self, nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo):
    def add_medical_record(self):
        # Trasmissione della transazione al contratto

        greeting_transaction = self.medico_contract.functions.addValues("Mario", "alta").build_transaction(
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
        print("Updating stored Value...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

        if tx_receipt.status == 1:
            # Transaction successful, retrieve updated values
            updated_values = self.medico_contract.functions.retrieve().call()
            print(f"Updated Stored Values: {updated_values}")
        else:
            print("Transaction failed or reverted")



        """         
        tx_hash = self.medico_contract.functions.addMedicalRecord(nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo).transact({'from': self.web3.eth.defaultAccount})
        # Attendere la conferma della transazione
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash) """
        return tx_receipt