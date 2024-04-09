from web3 import Web3
import json

import web3

from controllers.Exceptions.IntegrityCheckError import IntegrityCheckError
from controllers.utilities import Utilities
from database.db import db
from deploy import Deploy
import hashlib

class ControllerMedico:

    _instance = None
    def __init__(self):

        self.valoriHashContratto = []
        
        self.ut = Utilities()
        deploy = Deploy("MedicoContract.sol")
        self.abi, self.bytecode, self.w3, self.chain_id, self.my_address, self.private_key = deploy.create_contract()

        MedicoContract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        # Get the latest transaction
        self.nonce = self.w3.eth.get_transaction_count(self.my_address)
        # Submit the transaction that deploys the contract
        transaction = MedicoContract.constructor().build_transaction(
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
        #self.ut.resetHashBlockchain(self)
        #self.utilities = utilities.Utilities()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls() #super().__new__(cls)
        return cls._instance

    def addVisitaMedica(self, DataOra, CFpaziente, TipoPrestazione, Dati, Luogo):
        IdMedico = self.database.ottieniDatiAuth()[0]['CF']
        nome_tabella = "visitaMedico"
        lista_dati = [CFpaziente, IdMedico, Dati, DataOra, TipoPrestazione, Luogo]
        
        try:
            self.database.addTupla(nome_tabella, *lista_dati)
            
            # Calcola l'hash dei dati
            hash = self.ut.hash_row(lista_dati)
           
            
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
        visite = [visita for visita in self.medico_contract.functions.retrieveHashVisita(CFMedico, CFpaziente).call()]

        # Converti i risultati ottenuti direttamente in una struttura comprensibile
        return visite

    
    def addCurato(self, CFpaziente):
        cursor = self.database.conn.cursor()

        IdMedico = self.database.ottieniDatiAuth()[0]['CF']

        if  not any((curato[0] == IdMedico and curato[1] ==CFpaziente )for curato in self.database.ottieniCurati()):
            self.database.addTupla("curato",IdMedico,CFpaziente)
            return True
        else:
            return False
        
    def addPatologia(self, IdCartellaClinica, NomePatologia, DataDiagnosi, InCorso):
        try:
            # Costruisci la tupla dei valori da inserire
            patologia = (IdCartellaClinica, NomePatologia, DataDiagnosi, InCorso)
            
            
            # Chiama il metodo addTupla di db.py per inserire la nuova patologia
            inserimento_riuscito_db = self.database.addTupla("patologie", *patologia)
            
            
            if(inserimento_riuscito_db):
                # La inserisco nella blockchain, nessun check di integrità tanto è nuova la patologia
                all_patologie = self.ottieniPatologiePaziente(IdCartellaClinica)
                for tupla_patologia in all_patologie:
                    if(tupla_patologia[1]==NomePatologia):
                        address = self.w3.eth.accounts[0]
                        self.medico_contract.functions.storeHashPatologie(IdCartellaClinica, self.ut.hash_row(tupla_patologia)).transact({'from': address})
                        return inserimento_riuscito_db


            # """IN PIU"""
            # listaPatologieDB = self.database.retrieve_all_rows("patologie")
            # for patologiaa in listaPatologieDB:
            #     print(f"HASH DAL DB = {self.ut.hash_row(patologiaa)}")
            # print("***********************************************")
            # listaPatologieBlockchain = self.medico_contract.functions.retrieveHashPatologie("CFPaziente2").call()
            # for pt in listaPatologieBlockchain:
            #     print(f"HASH BLOCKCHAIN = {pt}")
            # """in piu """

            # Restituisci True se l'inserimento è riuscito, False altrimenti
            #return inserimento_riuscito_db
            
        except Exception as e:
            print("Errore durante l'aggiunta della patologia:", e)
            return False
        
    def ottieniPatologiePaziente(self, CFpaziente):
        cursor = self.database.conn.cursor()
        #ganache_url = "HTTP://127.0.0.1:7545"
        #web3 = Web3(Web3.HTTPProvider(ganache_url))
        patologielist = []

        patologie = self.database.ottieniPatologie(CFpaziente)
        #address = web3.eth.accounts[0]
        #blockchain_hash = self.medico_contract.functions.retrieveHashFarmaco(CFpaziente).call({'from': address})

        for patologia in patologie:
            #for hash in blockchain_hash:
            #if self.ut.check_integrity(hash, farmaco):
            patologielist.append(patologia)
        return patologielist
        
    def addCartellaClinica(self, CFpaziente):
        try:
            # Verifica se esiste già una cartella clinica per il paziente
            if not any((cartella[0] == CFpaziente) for cartella in self.database.ottieniCartelle()):
                # Crea una nuova cartella clinica nel database
                inserimento_riuscito = self.database.addTupla("cartellaClinica", CFpaziente, "", "")
                if inserimento_riuscito:
                    # Ottieni la tupla della cartella clinica dal database
                    tupla_cartella = self.database.ottieniCartellaFromCF(CFpaziente)
                    # Calcola l'hash della tupla della cartella clinica
                    hash_tupla = self.ut.hash_row(tupla_cartella)
                    # Ottieni l'indirizzo dell'account Ethereum da utilizzare per la transazione
                    address = self.w3.eth.accounts[0]
                    #print("hash tupla iniziale: " + hash_tupla)
                    # Effettua la transazione per memorizzare l'hash della cartella clinica nel contratto medico
                    tx_hash = self.medico_contract.functions.storeHashCartellaClinica(CFpaziente, hash_tupla).transact({'from': address})
                    # Aggiungi l'hash della transazione alla lista dei valori hash del contratto
                    self.valoriHashContratto.append(tx_hash)
                    return True
                else:
                    return False
            else:
                # Se esiste già una cartella clinica per il paziente, restituisci False
                return False
        except Exception as e:
            print("Errore durante l'aggiunta della cartella clinica:", e)
            return False

    def updateCartellaClinica(self, CFpaziente, nomeCampo, nuovo_valore):
        cursor = self.database.conn.cursor()
        ganache_url = "HTTP://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))

        cartelle = self.database.ottieniCartelle()

        for cartella in cartelle:
            #print(f"Hash tupla blockchain: {self._get_cartella_clinica_from_CF(CFpaziente)}")
            #print(f"Hash tuola database: {self.ut.hash_row(cartella)}")
            if cartella[0] == CFpaziente and self.ut.check_integrity(self._get_cartella_clinica_from_CF(CFpaziente), cartella):

                update_query = f"""
                    UPDATE cartellaClinica
                    SET {nomeCampo} = %s
                    WHERE CFpaziente = %s
                    """
                cursor.execute(update_query, (nuovo_valore, CFpaziente))
                self.database.conn.commit()
                cartellaAggiornato = self.database.ottieniCartellaFromCF(CFpaziente)
                new_hash = self.ut.hash_row(cartellaAggiornato)
                tx_hash = self.ut.modify_hash(self.medico_contract,CFpaziente, new_hash,self)                    
                self.valoriHashContratto.append(tx_hash)
                print(f"Aggiornamento di {nomeCampo} con successo.")
                return True
        return False
    
    def ottieniFarmacoPaziente(self, CFpaziente):
        cursor = self.database.conn.cursor()
        ganache_url = "HTTP://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        medicinali = []

        farmaci = self.database.ottieniFarmaci(CFpaziente)
        address = web3.eth.accounts[0]
        blockchain_hash = self.medico_contract.functions.retrieveHashFarmaco(CFpaziente).call({'from': address})

        for farmaco in farmaci:
            for hash in blockchain_hash:
                if self.ut.check_integrity(hash, farmaco):
                    medicinali.append(farmaco)
        return medicinali

                    
    def addFarmaco(self, IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio):
        try:
            # Verifica se esiste già un farmaco con lo stesso nome nella cartella clinica specificata
            if not any((farmaco[0] == IdCartellaClinica and farmaco[1] == NomeFarmaco) for farmaco in self.database.ottieniFarmaci(IdCartellaClinica)):
                # Crea una nuova tupla per il farmaco nel database
                inserimento_riuscito = self.database.addTupla("farmaci", IdCartellaClinica, NomeFarmaco, DataPrescrizione, Dosaggio)
                if inserimento_riuscito:
                    # Memorizza l'hash del farmaco nella blockchain
                    farmaco = self.database.ottieniFarmaco(IdCartellaClinica, NomeFarmaco)
                    hash_tupla = self.ut.hash_row(farmaco[0])
                    address = self.w3.eth.accounts[0]
                    self.medico_contract.functions.storeHashFarmaco(IdCartellaClinica, hash_tupla).transact({'from': address})
                    return True
                else:
                    return False
            else:
                # Se esiste già un farmaco con lo stesso nome nella cartella clinica specificata, restituisci False
                return False
        except Exception as e:
            print("Errore durante l'aggiunta del farmaco:", e)
            return False

    def visualizzaRecordVisite(self, CFPaziente):
        try:
            pazienti = self.database.ottieniDatiPaziente(CFPaziente)
            IdMedico = self.database.ottieniDatiAuth()[0]['CF']
            hash_visite = self.medico_contract.functions.retrieveHashVisita(IdMedico, CFPaziente).call()
            if pazienti:
                for index, paziente in enumerate(pazienti):
                    print(f"Paziente selezionato: {paziente[1]} {paziente[2]}, {paziente[3]}")
                    visite = self.database.ottieniVisitePaziente(paziente[0], IdMedico)
                    print(f"Elenco delle visite effettuate per il paziente {paziente[0]}")
                    indice = 0
                    integrita_verificata = False
                    for visita in visite:
                        for hash_v in hash_visite:
                            if self.ut.check_integrity(hash_v, visita):
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

    def modificaDoseFarmaco(self, NuovaDose, tupla_farmaco):
        """Questo metodo permette la modifica del dosaggio di un farmaco, aggiornando il  DB
        e la blockchain"""
        # Ritorna una lista di hash di farmaci
        hash_farmaco_blockchain = self.medico_contract.functions.retrieveHashFarmaco(tupla_farmaco[0]).call()
        check = False
        for hash_bc in hash_farmaco_blockchain:
            if(self.ut.check_integrity(hash_bc, tupla_farmaco)):
                check = True
                break
        #self.database.modificaDosaggiofarmaco(IdCartella, NomeFarmaco, NuovaDose)           
        if (self.database.modificaDosaggiofarmaco(tupla_farmaco[0], tupla_farmaco[1], NuovaDose) and check):
            address = self.w3.eth.accounts[0]
            self.medico_contract.functions.storeHashFarmaco(tupla_farmaco[0], self.ut.hash_row(tupla_farmaco)).transact({'from': address})
            print("Dosaggio del farmaco modificato correttamente")
            return True
        else:
            print("Modifica non avvenuta")
            return False
    
    def modificaStatoPatologia(self, nuovoStato, tupla_patologia):
        try:
            all_patologie = self.ottieniPatologiePaziente(tupla_patologia[0])
            for tupla in all_patologie:
                if(tupla[1]==tupla_patologia[1]):
                    all_tuple_blockchain = self.medico_contract.functions.retrieveHashPatologie(tupla[0]).call()
                    for tupla_blockchain in all_tuple_blockchain:
                        if(self.ut.check_integrity(tupla_blockchain,tupla)):
                            self.database.modificaStatoPatologia(tupla_patologia[0], tupla_patologia[1], nuovoStato)
                            address = self.w3.eth.accounts[0]
                            self.medico_contract.functions.storeHashPatologie(tupla[0],self.ut.hash_row(tupla)).transact({'from': address})
                            print("HASH CORRETTAMENTE SALVATO IN BLOCKCHAIN !")
                            return True
                    raise IntegrityCheckError("Integrità dati PATOLOGIE non rispettata")
        
        except IntegrityCheckError as e:
            print(e)
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
    

    