from web3 import Web3
import json

from controllers.utilities import Utilities
from database.db import db
from deploy import Deploy
import hashlib

class ControllerMedico:
    def __init__(self):

        deploy = Deploy("Visita.sol")
        self.abi, self.bytecode, self.w3, self.chain_id, self.my_address, self.private_key = deploy.create_contract()

        Visita = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        # Get the latest transaction
        self.nonce = self.w3.eth.get_transaction_count(self.my_address)
        # Submit the transaction that deploys the contract
        transaction = Visita.constructor().build_transaction(
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

        # Attivo lo smart contract: "Cartella Clinica"
        self.cartella_clinica = self._deploy_cartella_clinica("CartellaClinica")
        self.database = db()
        #self.utilities = utilities.Utilities()

    def _deploy_cartella_clinica(self, nomeSmartContract):
        deploy = Deploy(f"{nomeSmartContract}.sol")
        abi, bytecode, w3, chain_id, my_address, private_key = deploy.create_contract()

        Visita = w3.eth.contract(abi=abi, bytecode=bytecode)
        # Get the latest transaction
        nonce = w3.eth.get_transaction_count(my_address)
        # Submit the transaction that deploys the contract
        transaction = Visita.constructor().build_transaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        #print("Deploying Contract!")
        # Send it!
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        #print("Waiting for transaction to finish...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        #print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

        # Working with deployed Contracts
        contratto = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

        return contratto
        #self.utilities = utilities.Utilities()

    def addVisitaMedica(self, DataOra, CFpaziente, TipoPrestazione, Dati, Luogo):
        cursor = self.database.conn.cursor()

        IdMedico = self.database.ottieniDatiAuth()[0]['CF']

        nome_tabella = "visitaMedico"

        insert_query = f"""
        INSERT INTO {nome_tabella} (CFPaziente, CFMedico, Dati, DataOra, TipoPrestazione, Luogo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Dati da inserire nella visita medica
        data_visita = (CFpaziente, IdMedico, Dati, DataOra, TipoPrestazione, Luogo)

        # Esecuzione dell'istruzione per inserire la visita medica
        cursor.execute(insert_query, data_visita)

        # Commit delle modifiche
        self.database.conn.commit()

        lista_dati = [CFpaziente, IdMedico, Dati, DataOra, TipoPrestazione, Luogo]
        hash = self.hash_row(lista_dati)
        print(hash)

        # Chiusura del cursore e della connessione
        

        # Chiamata alla funzione storeHash del contratto Visita
        greeting_transaction = self.medico_contract.functions.storeHash(IdMedico, CFpaziente, hash).build_transaction(
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

        visite = self.getVisiteMedico(CFpaziente)

        """ cursor.close()
        self.database.conn.close() """

        return visite

    def getVisiteMedico(self, CFpaziente):
        # Ottieni l'ID del medico
        CFMedico = self.database.ottieniDatiAuth()[0]['CF']

        # Chiamata alla funzione retrieveHash del contratto Visita
        visite = self.medico_contract.functions.retrieveHash(CFMedico, CFpaziente).call()

        # Converti i risultati ottenuti in una struttura comprensibile
        visite_comprensibili = []
        for visita in visite:
            # Qui puoi fare ulteriori elaborazioni se necessario
            visite_comprensibili.append(visita)
            print(visita)

        return visite_comprensibili
    
    def addCurato(self, CFpaziente):
        cursor = self.database.conn.cursor()

        IdMedico = self.database.ottieniDatiAuth()[0]['CF']

        if  not any((curato[0] == IdMedico and curato[1] ==CFpaziente )for curato in self.database.ottieniCurati()):
            nome_tabella = "curato"

            print('ciao')

            insert_query = f"""
            INSERT INTO {nome_tabella} (CFPaziente, CFMedico)
            VALUES (%s, %s)
            """
            nuovo_curato = (CFpaziente, IdMedico)

            cursor.execute(insert_query, nuovo_curato)

            self.database.conn.commit()

            self.addCartellaClinica(CFpaziente)
            
            """ cursor.close()
            self.database.conn.close() """

            return True
        else:
            return False
        
    def addPatologia(self, IdCartellaClinica, NomePatologia, DataDiagnosi, InCorso):
        cursor = self.database.conn.cursor()
        
        if  not any((patologia[0] == IdCartellaClinica and patologia[1] == NomePatologia )for farmaco in self.database.ottieniPatologie()):

            nome_tabella = "patologie"

            insert_query = f"""
            INSERT INTO {nome_tabella} (IdCartellaClinica, NomePatologia, DataDiagnosi, InCorso)
            VALUES (%s, %s, %s, %s)
            """

            # Dati da inserire nella visita medica
            patologia = (IdCartellaClinica, NomePatologia, DataDiagnosi, InCorso)
            print(patologia)

            # Esecuzione dell'istruzione per inserire la visita medica
            cursor.execute(insert_query, patologia)

            # Commit delle modifiche
            self.database.conn.commit()
            
            "cursor.close()"
            "self.database.conn.close()"

            return True
        else:
            return False
        
        
        
    def addCartellaClinica(self, CFpaziente):
        cursor = self.database.conn.cursor()

        if  not any((cartella[0] == CFpaziente )for cartella in self.database.ottieniCartelle()):
            ut = Utilities()
            nome_tabella = "cartellaClinica"

            insert_query = f"""
            INSERT INTO {nome_tabella} (CFPaziente)
            VALUES (%s)
            """
            nuova_cartella = (CFpaziente,)

            cursor.execute(insert_query, nuova_cartella)

            self.database.conn.commit()

            # Ora occorre aggiungere l'hash alla blockchain. Per farlo riprendiamo la tupla
            tupla = self.database.ottieniCartellaFromCF(CFpaziente)
            hash_tupla = ut.hash_row(tupla[0])

            #contract_address = "0x94324c9C4F1D1786a38Cd9CF6c54f230f25aE7Eb" #self.cartella_clinica.address
                    #my_address = "0x94324c9C4F1D1786a38Cd9CF6c54f230f25aE7Eb"
            accounts = self.w3.eth.accounts
            address = accounts[0]
            

            self.cartella_clinica.functions.storeHash(CFpaziente, hash_tupla).transact({'from': address})
            """ cursor.close()
            self.database.conn.close() """

            hashes = self.cartella_clinica.functions.retrieveHash(CFpaziente).call()

            return True
        else:
            return False
    
    def updateCartellaClinica(self, CFpaziente, nomeCampo, nuovo_valore):
        cursor = self.database.conn.cursor()
        ut = Utilities()
        

        # Se il paziente esiste ma non ha una cartella clinica, ne viene creata una provvisoria e viene
        # aggiunto l'hash nella blockchain        
        adding = self.addCartellaClinica(CFpaziente)
        cartelle = self.database.ottieniCartelle()
        
        
        # Check per verificare che è stata ruspettata l'integrità del dato
        for cartella in cartelle:
            if(cartella[0] == CFpaziente):
                #print(self._get_cartella_clinica_from_CF(CFpaziente) + " ** " + cartella + " ** " + ut.hash_row(cartella))
                if(ut.check_integrity(self._get_cartella_clinica_from_CF(CFpaziente), cartella)):
                    update_query = f"""
                        UPDATE cartellaClinica
                        SET {nomeCampo} = %s
                        WHERE CFpaziente = %s
                        """
                    cursor.execute(update_query, (nuovo_valore, CFpaziente))
                    # Commit delle modifiche al database
                    self.database.conn.commit()
                    cartellaAggiornato = self.database.ottieniCartellaFromCF(CFpaziente)[0]
                    new_hash = ut.hash_row(cartellaAggiornato)
                    ut.modify_hash(self.cartella_clinica, CFpaziente, new_hash,self)
                    print(f"Aggiornamento di {nomeCampo} con successo.")
                    return True
                return False             
        


        # Salvataggio delle modifiche
        #conn.commit()

        # Chiusura della connessione
        #conn.close()
                
        return False

        
        #else:
            #return False
    
    def addFarmaco(self, IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio):
        
        cursor = self.database.conn.cursor()
        
        if  not any((farmaco[0] == IdCartellaClinica and farmaco[1] == NomeFarmaco )for farmaco in self.database.ottieniFarmaci()):

            nome_tabella = "farmaci"

            insert_query = f"""
            INSERT INTO {nome_tabella} (IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio)
            VALUES (%s, %s, %s, %s)
            """

            # Dati da inserire nella visita medica
            farmaco = (IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio)
            print(farmaco)

            # Esecuzione dell'istruzione per inserire la visita medica
            cursor.execute(insert_query, farmaco)

            # Commit delle modifiche
            self.database.conn.commit()

            # Inserisco la nuova cartella clinica 
            
            "cursor.close()"
            "self.database.conn.close()"

            return True
        else:
            return False


    def pazientiCurati(self):
        medico_cf = self.database.ottieniDatiAuth()[0]['CF']
        #Ottengo la lista di tuple riprese dalla tabella curato in cui CFMedico è uguale al Cf del medico che ha fatto l'accesso
        return filter(lambda curato: curato[0] == medico_cf, self.database.ottieniCurati())

    def datiPazientiCurati(self):
        #Ottengo la lista di dati effettivi dei pazienti curati dal medico che ha fatto l'accesso
        return map(lambda pazienteCurato: self.database.ottieniDatiPaziente(pazienteCurato[1]), self.pazientiCurati())

    def hash_row(self, sql_row):
        row_string = ','.join(map(str, sql_row))

        hash_object = hashlib.md5()

        hash_object.update(row_string.encode())

        hash_result = hash_object.hexdigest()

        return hash_result

        #sql_row = [1, 'John', 'Doe', 'john.doe@example.com']
    
    def _get_cartella_clinica_from_CF(self,cf):
        try:
            # Chiama la funzione retrieveHash del contratto
            hashes = self.cartella_clinica.functions.retrieveHash(cf).call()
            #print(str(hashes))
            return hashes
        except Exception as e:
            print(f"Errore durante il recupero degli hash: {e}")
            return None