import hashlib

import web3

from database.db import db

class Utilities:

    _db = db()

    def hash_row(self,sql_row):
        row_string = ','.join(map(str, sql_row))
        #print(f"sql_row {row_string}")
        hash_object = hashlib.md5()

        hash_object.update(row_string.encode())
        #print(f"sql_row {hash_object}")

        hash_result = hash_object.hexdigest()
        #print(f"sql_row {hash_result}")

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

    def resetHashBlockchain(self, controller):
        """"Questo metodo re-setta gli hash nella blockchain"""
        self._resetHashCartellaClinica(controller)
        self._resetHashFarmaci(controller)
        self._resetHashVisiteMedico(controller)
        self._resetHashPatologie(controller)
        


    def _resetHashCartellaClinica(self,controller):
        """Re-inserisco gli hash nella cartella clinica"""
        tuple_cartella_clinica = self._db.ottieniCartelle()
        address = controller.w3.eth.accounts[0]       
        for tupla in tuple_cartella_clinica:
            hash_tupla = self.hash_row(tupla)
            #print(f"Hash tupla salvata {hash_tupla}")
            # Salvo nella blockchain
            controller.medico_contract.functions.storeHashCartellaClinica(tupla[0], hash_tupla).transact({'from': address})
    
    def _resetHashFarmaci(self,controller):
        """Re-inserisco gli hash di tutti i farmaci dei vari pazineti nello smart contract"""
        tupleFarmaci = self._db.retrieve_all_rows("farmaci")
        address = controller.w3.eth.accounts[0]   
        for tupla in tupleFarmaci:
            hash_farmaco = self.hash_row(tupla)
            controller.medico_contract.functions.storeHashFarmaco(tupla[0], hash_farmaco).transact({'from': address})
    
    def _resetHashVisiteMedico(self,controller):
        """Re-inserisco gli hash di tutte le visite-mediche effettuate nello smart contract"""
        tuple_visite = self._db.retrieve_all_rows("visitaMedico")
        address = controller.w3.eth.accounts[0]
        for tupla in tuple_visite:
            hash_visita = self.hash_row(tupla)
            controller.medico_contract.functions.storeHashVisita(tupla[1],tupla[0],hash_visita).transact({'from': address})
    
    def _resetHashPatologie(self,controller):
        """Re-inserisco tutti gli hash riferiti alla tabella PATOLOGIE nella blockchain"""
        tuplePatologie = self._db.retrieve_all_rows("patologie")
        address = controller.w3.eth.accounts[0]   
        for tupla in tuplePatologie:
            hash_patologia = self.hash_row(tupla)
            controller.medico_contract.functions.storeHashPatologie(tupla[0], hash_patologia).transact({'from': address})


        

        


    
