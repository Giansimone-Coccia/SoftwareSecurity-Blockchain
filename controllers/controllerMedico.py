from web3 import Web3
import json

import web3

from controllers.utilities import Utilities
from database.db import db
from deploy import Deploy
import hashlib

class ControllerMedico:
    def __init__(self):

        self.valoriHashContratto = []

        self.ut = Utilities()
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
        #self.cartella_clinica = self._deploy_cartella_clinica("CartellaClinica")
        self.database = db()
        #self.utilities = utilities.Utilities()

    def addVisitaMedica(self, DataOra, CFpaziente, TipoPrestazione, Dati, Luogo):
        IdMedico = self.database.ottieniDatiAuth()[0]['CF']
        nome_tabella = "visitaMedico"
        lista_dati = [CFpaziente, IdMedico, Dati, DataOra, TipoPrestazione, Luogo]
        
        try:
            self.database.addTupla(nome_tabella, *lista_dati)
            
            # Calcola l'hash dei dati
            hash = self.ut.hash_row(lista_dati)
            print(hash)
            
            # Chiamata al contratto medico per memorizzare l'hash
            greeting_transaction = self.medico_contract.functions.storeHashVisita(IdMedico, CFpaziente, hash).build_transaction(
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

            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
            self.nonce += 1
            
            # Ottieni e restituisci le visite mediche del paziente
            visite = self.getVisiteMedico(CFpaziente)
            return visite
        
        except Exception as e:
            print("Errore durante l'aggiunta della visita medica:", e)


    def getVisiteMedico(self, CFpaziente):
        # Ottieni l'ID del medico
        CFMedico = self.database.ottieniDatiAuth()[0]['CF']

        # Chiamata alla funzione retrieveHash del contratto Visita
        visite = self.medico_contract.functions.retrieveHashVisita(CFMedico, CFpaziente).call()

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
            self.database.addTupla("curato",IdMedico,CFpaziente)
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

            patologia = (IdCartellaClinica, NomePatologia, DataDiagnosi, InCorso)
            print(patologia)

            cursor.execute(insert_query, patologia)

            self.database.conn.commit()

            return True
        else:
            return False
        
    def addCartellaClinica(self, CFpaziente):
        cursor = self.database.conn.cursor()

        if  not any((cartella[0] == CFpaziente )for cartella in self.database.ottieniCartelle()):
            nome_tabella = "cartellaClinica"

            insert_query = f"""
            INSERT INTO {nome_tabella} (CFPaziente)
            VALUES (%s)
            """
            nuova_cartella = (CFpaziente,)

            cursor.execute(insert_query, nuova_cartella)

            self.database.conn.commit()

            tupla = self.database.ottieniCartellaFromCF(CFpaziente)
            hash_tupla = self.ut.hash_row(tupla[0])

            accounts = self.w3.eth.accounts
            address = accounts[0]
            

            tx_hash = self.medico_contract.functions.storeHashCartellaClinica(CFpaziente, hash_tupla).transact({'from': address})
            self.valoriHashContratto.append(tx_hash)

            return True
        else:
            return False
    
    def updateCartellaClinica(self, CFpaziente, nomeCampo, nuovo_valore):
        cursor = self.database.conn.cursor()
        ganache_url = "HTTP://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))

        adding = self.addCartellaClinica(CFpaziente)
        cartelle = self.database.ottieniCartelle()

        for cartella in cartelle:
            print(cartella)
            if cartella[0] == CFpaziente and self.ut.check_integrity(self._get_cartella_clinica_from_CF(CFpaziente), cartella):
                update_query = f"""
                    UPDATE cartellaClinica
                    SET {nomeCampo} = %s
                    WHERE CFpaziente = %s
                    """
                cursor.execute(update_query, (nuovo_valore, CFpaziente))
                self.database.conn.commit()
                cartellaAggiornato = self.database.ottieniCartellaFromCF(CFpaziente)[0]
                new_hash = self.ut.hash_row(cartellaAggiornato)
                tx_hash = self.ut.modify_hash(self.medico_contract, CFpaziente, new_hash,self)                    
                self.valoriHashContratto.append(tx_hash)
                print(f"Aggiornamento di {nomeCampo} con successo.")
                return True
        return False
                    
    def addFarmaco(self, IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio):
        
        cursor = self.database.conn.cursor()
        
        if  not any((farmaco[0] == IdCartellaClinica and farmaco[1] == NomeFarmaco )for farmaco in self.database.ottieniFarmaci()):

            nome_tabella = "farmaci"

            insert_query = f"""
            INSERT INTO {nome_tabella} (IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio)
            VALUES (%s, %s, %s, %s)
            """

            farmaco = (IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio)
            print(farmaco)

            cursor.execute(insert_query, farmaco)

            self.database.conn.commit()

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

    def _get_cartella_clinica_from_CF(self,cf):
        try:
            # Chiama la funzione retrieveHash del contratto
            hashes = self.medico_contract.functions.retrieveHashCartellaClinica(cf).call()
            print(str(hashes))
            return hashes
        except Exception as e:
            print(f"Errore durante il recupero degli hash: {e}")
            return None
        
    def visualizza_contenuto_contratto(self,contratto, tx_receipt):
        # Ottieni l'evento 'ContentSet' dal contratto
        event = contratto.events.ContentSet()

        # Ottieni il contenuto utilizzando la ricevuta di transazione
        event_filter = event.processReceipt(tx_receipt)
        contenuto = event_filter[0]['args']['content']

        return contenuto
    
    def visualizzaTuttiRecordMedici(self):
        # indichiamo qual'è il CF del medico loggato
        CFMedico = self.database.ottieniDatiAuth()[0]['CF']

        visite = self.database.ottieniDatiVisite(CFMedico)
        for visita in visite:
            print("***********************************")
            print("* Codice fiscale paziente: " + visita[0] )
            print("* Dati: " + visita[2] )
            print("* Data e Ora: " + visita[3].strftime("%Y-%m-%d %H:%M:%S") )
            print("* Prestazione fornita: " + visita[4] )
            print("* Luogo visita: " + visita[5] )
            print("***********************************")
