import hashlib

import web3

class Utilities:

    def hash_row(self,sql_row):
        row_string = ','.join(map(str, sql_row))

        hash_object = hashlib.md5()

        hash_object.update(row_string.encode())

        hash_result = hash_object.hexdigest()

        return hash_result

    #sql_row = [1, 'John', 'Doe', 'john.doe@example.com']



    def check_integrity(self,blockchain_hash, to_check):
        """Prende in input l'hash nella blockchain e la tupla su cui fare il check
        Attenzione : il to_check è la tupla non l'hash della tupla """
        hash_to_check = self.hash_row(to_check)
        return blockchain_hash == hash_to_check
    
    
    def modify_hash(self,contratto, codice_fiscale_paziente, new_hash, controller):
        try:
            # Chiama la funzione modifyHash del contratto
            accounts = controller.w3.eth.accounts
            address = accounts[0]
            tx_hash = contratto.functions.modifyHashCartellaClinica(codice_fiscale_paziente, new_hash).transact({'from': address})
            return tx_hash
        except Exception as e:
            print(f"Errore durante la modifica dell'hash: {e}")


    
