
import logging
import os
import re
from dotenv import load_dotenv
import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from datetime import datetime
from Exceptions.SQLInjectionError import SQLInjectionError
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from interface.Ilog import Ilog

class db(Ilog):

    def __init__(self):
        # Parametri di connessione al database
        self.logging = logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        config = {
            'user': 'progettoss',
            'password': 'Blockchain@!456',
            'host': 'db4free.net',
            'database': 'softwaresecurity',
            'port': '3306',
            'raise_on_warnings': True  # Opzionale, solleva un'eccezione su avvisi MySQL
        }

        self.port = config['port']

        load_dotenv("Chiavi.env")
        self.key = os.getenv("PRIVATE_KEY_DEC_ENC_DB") # Chiave da usare anche nel db 
        try:
            # Connessione al database
            self.conn = mysql.connector.connect(**config)
              

        except mysql.connector.Error as err:
            print("Errore di connessione al database:", err)

        finally:
            # Chiudi la connessione
            if 'conn' in locals() and self.conn.is_connected():
                self.conn.close()
    
    def log_actions(func):
        """Implementazione di un decorator per il logger"""
        def wrapper(self, *args, **kwargs):
            logging.info(f"{self.__class__.__name__}: Chiamato {func.__name__} , Porta: {self.port}")
            return func(self, *args, **kwargs)
        return wrapper
    
    def _sqlInjectionCheck(*params):
        """Controlla la presenza di potenziali SQL injection nei parametri."""
        # Espressione regolare per cercare caratteri che potrebbero indicare una query SQL
        sql_pattern = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|OR|AND|UNION|DROP|ALTER|EXEC)\b', re.IGNORECASE)

        for param in params:
            if re.search(sql_pattern, str(param)):
                raise SQLInjectionError("Potenziale SQL injection rilevata.")
    
    @log_actions
    def ottieniDatiAuth(self):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'autenticazione'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        query = f"SELECT AES_DECRYPT(CF,'{self.key}'), AES_DECRYPT(Username,'{self.key}'), AES_DECRYPT(Password,'{self.key}'), AES_DECRYPT(Ruolo,'{self.key}') FROM {table_name}"
        cursor.execute(query)
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        # Stampa i valori decodificati per ogni tupla
        utenti = []
        for tupla in rows:
            CF_decoded = tupla[0].decode('utf-8') if tupla[0] is not None else None
            Username_decoded = tupla[1].decode('utf-8') if tupla[1] is not None else None
            Password_decoded = tupla[2].decode('utf-8') if tupla[2] is not None else None
            Ruolo_decoded = tupla[3].decode('utf-8') if tupla[3] is not None else None

            tuplaDict = {'CF': CF_decoded, 'Username': Username_decoded,
                        'Password': Password_decoded, 'Ruolo': Ruolo_decoded}
            utenti.append(tuplaDict)

        return utenti
    
    @log_actions
    def ottieniCurati(self):
        try:
            # Nome della tabella da cui desideri recuperare i dati
            table_name = 'curato'
            cursor = self.conn.cursor()
            # Esegui una query per selezionare tutti i dati dalla tabella specificata
            cursor.execute(f"SELECT * FROM {table_name}")
            # Recupera tutte le tuple
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            print(f"ERRORE ! {err}")
            return []
    
    @log_actions
    def ottieniAssistiti(self):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'assistito'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name}")
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    @log_actions
    def ottieniCartelle(self):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'cartellaClinica'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name}")
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    @log_actions
    def ottieniCartellaFromCF(self,cf):
        # Nome della tabella da cui desideri recuperare i dati
        self._sqlInjectionCheck(cf)
        table_name = 'cartellaClinica'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = '{cf}'")
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows[0]
    
    @log_actions
    def ottieniVisitePaziente(self, CFPaziente, CFMedico):
        self._sqlInjectionCheck(CFPaziente, CFMedico)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'visitaMedico'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = %s AND CFMedico = %s", (CFPaziente, CFMedico))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    @log_actions
    def ottieniVisiteMedico(self, CFPaziente, CFMedico):
        self._sqlInjectionCheck(CFPaziente, CFMedico)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'visitaMedico'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = %s AND CFMedico = %s", (CFPaziente, CFMedico))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    @log_actions
    def ottieniVisiteOS(self, CFPaziente, CFOperatore):
        self._sqlInjectionCheck(CFPaziente, CFOperatore)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'visitaOperatore'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = %s AND CFOperatoreSanitario = %s", (CFPaziente, CFOperatore))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows

    @log_actions
    def ottieniFarmaci(self, CF):
        self._sqlInjectionCheck(CF)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'farmaci'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE IdCartellaClinica = %s", (CF,))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    @log_actions
    def ottieniFarmaco(self, CF, nomeFarmaco):
        self._sqlInjectionCheck(CF, nomeFarmaco)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'farmaci'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE IdCartellaClinica = %s AND NomeFarmaco = %s", (CF, nomeFarmaco))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    @log_actions
    def modificaDosaggiofarmaco(self, CF, nomeFarmaco, dosaggio):
        try:
            self._sqlInjectionCheck(CF, nomeFarmaco, dosaggio)
            # Nome della tabella da cui desideri recuperare i dati
            table_name = 'farmaci'
            cursor = self.conn.cursor()         
            # Esegui una query per aggiornare il dosaggio del farmaco nella tabella specificata
            cursor.execute(f"UPDATE {table_name} SET Dosaggio = %s WHERE IdCartellaClinica = %s AND NomeFarmaco = %s", (dosaggio, CF, nomeFarmaco))
            # Commit delle modifiche al database
            self.conn.commit()
            # Verifica se è stata effettuata almeno una modifica
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            # Gestione degli errori
            print("Errore durante la modifica del dosaggio del farmaco:", e)
            return False
    
    @log_actions
    def modificaStatoPatologia(self, CF, nomePatologia, stato):
        try:
            self._sqlInjectionCheck(CF, nomePatologia, stato)
            # Nome della tabella da cui desideri recuperare i dati
            table_name = 'patologie'
            cursor = self.conn.cursor()         
            # Esegui una query per aggiornare il dosaggio del farmaco nella tabella specificata
            cursor.execute(f"UPDATE {table_name} SET InCorso = %s WHERE IdCartellaClinica = %s AND NomePatologia = %s", (stato, CF, nomePatologia))
            # Commit delle modifiche al database
            self.conn.commit()
            # Verifica se è stata effettuata almeno una modifica
            # Definizione di una lambda function per filtrare le righe
            filter_func = lambda row: row[0] == CF and row[1] == nomePatologia and row[3] == stato

            # Recupero di tutte le righe dalla tabella
            all_rows = self.retrieve_all_rows(table_name)

            # Filtraggio delle righe usando la lambda function
            filtered_rows = list(filter(filter_func, all_rows))

            if(len(filtered_rows) != 0):
                return filtered_rows[0]
            else:
                return ()
        except Exception as e:
            # Gestione degli errori
            print("Errore durante la modifica dello stato della patologia:", e)
            return ()

    @log_actions
    def ottieniPatologie(self, CF):
        self._sqlInjectionCheck(CF)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'patologie'
    
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE IdCartellaClinica = %s", (CF,))

        # Recupera tutte le tuple
        rows = cursor.fetchall()

        return rows
    
    @log_actions
    def ottieniDatiUtente(self, nomeTabella, CF):
        self._sqlInjectionCheck(nomeTabella, CF)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = nomeTabella
        cursor = self.conn.cursor()
        # Esegui una query per selezionare solo le righe con il CF specificato
        cursor.execute(f"SELECT * FROM {table_name} WHERE CF = %s", (CF,))
        # Recupera le righe filtrate
        rows = cursor.fetchall()
        return rows
    
    @log_actions
    def ottieniCartellaClinicaPaziente(self, CF):
        self._sqlInjectionCheck(CF)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'caretllaClinica'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare solo le righe con il CF specificato
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = %s", (CF,))
        # Recupera le righe filtrate
        rows = cursor.fetchall()
        return rows

    @log_actions
    def gestisciAccesso(self,username,password):
        utenti = self.ottieniDatiAuth()
        for u in utenti:
              if(u['Username']==username and u['Password']==password):
                  return True
        
        return False
    
    @log_actions
    def ottieniProfessione(self,username,password):
         utenti = self.ottieniDatiAuth()

         for utente in utenti:
              if(utente['Username'] == username and utente['Password'] == password):
                return utente['Ruolo']
    
    @log_actions
    def ottieniCF(self,username,password):
         utenti = self.ottieniDatiAuth()

         for utente in utenti:
              if(utente['Username'] == username and utente['Password'] == password):
                return utente['CF']

    @log_actions
    def addTupla(self, nomeTabella, *valori):
        try:
            # Crea un cursore dalla connessione al database
            cursor = self.conn.cursor()

            cursor.execute("SELECT * FROM {} LIMIT 1".format(nomeTabella))
            colonne = [desc[0] for desc in cursor.description]
            # Leggi tutti i risultati della query SELECT
            cursor.fetchall()
            # Costruisci la query di inserimento dinamica
            query = f"INSERT INTO {nomeTabella} ({', '.join(colonne)}) VALUES ({', '.join(['%s'] * len(colonne))})"
            print(query)
            # Esegui l'inserimento
            cursor.execute(query, valori)
            self.conn.commit()
            print("Nuova tupla inserita correttamente")
            return True
        except mysql.connector.Error as err:
            print("Errore durante l'aggiunta della tupla:", err)
            return False
        finally:
            # Chiudi il cursore
            cursor.close()

    @log_actions
    def fromValueToId(self, nomeTabella, input_value):
        try:
            self._sqlInjectionCheck(nomeTabella)
            # Crea un cursore dalla connessione al database
            cursor = self.conn.cursor()
            # Esegui una query per selezionare tutte le tuple dalla tabella specificata
            cursor.execute(f"SELECT * FROM {nomeTabella}")
            # Recupera tutte le tuple
            rows = cursor.fetchall()
            # Cerca il primo valore della prima tupla in cui è presente l'input
            for tupla in rows:
                if input_value in tupla:
                    # Ritorna il primo valore della tupla
                    return tupla[0]
            # Se non viene trovata nessuna tupla con l'input, ritorna None
            return None
        except mysql.connector.Error as err:
            print("Errore durante l'accesso ai dati:", err)
        finally:
            # Chiudi il cursore
            cursor.close()

    @log_actions
    def retrieve_all_rows(self,table_name):
        """
        Metodo per recuperare tutte le tuple da una tabella nel database.

        Args:
            table_name (str): Il nome della tabella da cui recuperare le tuple.
            conn (sqlite3.Connection): Oggetto di connessione al database.

        Returns:
            list: Una lista di tuple rappresentanti le righe della tabella.
        """
        try:
            self._sqlInjectionCheck(table_name)
            cursor = self.conn.cursor()
            # Esecuzione della query per recuperare tutte le tuple dalla tabella
            cursor.execute(f"SELECT * FROM {table_name}")
            # Recupero di tutte le righe dalla query
            rows = cursor.fetchall()
        except mysql.connector.Error as err:
            print("Errore durante l'accesso ai dati:", err)
        finally:
            # Chiudi il cursore
            cursor.close()
        return rows
    
    @log_actions
    def updateCartellaClinica(self, CF, nuovo_trattamento):
        self._sqlInjectionCheck(CF, nuovo_trattamento)
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'cartellaClinica'
        cursor = self.conn.cursor()
        try:
            # Esegui una query per aggiornare il campo "Trattamento" per il paziente con il CF specificato
            cursor.execute(f"UPDATE {table_name} SET Trattamento = %s WHERE CF = %s", (nuovo_trattamento, CF))
            # Conferma la transazione
            self.conn.commit()
            # Ottieni il numero di righe aggiornate
            num_rows_updated = cursor.rowcount
            return num_rows_updated
        except Exception as e:
            # Annulla eventuali modifiche in caso di errore
            self.conn.rollback()
            print("Si è verificato un errore durante l'aggiornamento della cartella clinica:", e)
            return 0
        finally:
            # Chiudi il cursore
            cursor.close()

    @log_actions
    def addNuovoPaziente(self, cf, nome, cognome, residenza):
        self._sqlInjectionCheck(cf, nome, cognome, residenza)
        # Nome della tabella in cui inserire i nuovi dati
        table_name = 'paziente'
        cursor = self.conn.cursor()
        try:
            # Esegui una query per inserire i nuovi dati nella tabella paziente
            cursor.execute(f"INSERT INTO {table_name} (CF, Nome, Cognome, Residenza) VALUES (%s, %s, %s, %s)", (cf, nome, cognome, residenza))
            # Conferma la transazione
            self.conn.commit()
            # Ottieni il numero di righe inserite
            num_rows_inserted = cursor.rowcount
            print("Paziente registrato con successo")
            return num_rows_inserted
        except Exception as e:
            # Annulla eventuali modifiche in caso di errore
            self.conn.rollback()
            print("Si è verificato un errore durante l'inserimento dei dati del paziente:", e)
            return 0
        finally:
            # Chiudi il cursore
            cursor.close()
    
    @log_actions
    def eliminaVisitaOS(self, visita):
        table_name = 'visitaOperatore'
        cursor = self.conn.cursor()

        try:
            # Esegui la query per eliminare la visita
            query = f"DELETE FROM {table_name} WHERE CFPaziente = %s AND CFOperatoreSanitario = %s AND DataOra = %s"
            
            # Converti la stringa in un oggetto datetime
            #data_ora_str = visita[3][18:-1]  # Estrai la parte di stringa contenente la data e l'ora effettive
            #data_ora_datetime = datetime.strptime(data_ora_str, "%Y, %m, %d, %H, %M, %S")  # Converte la stringa in un oggetto datetime
            #data_ora_formattata = data_ora_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Formatta la data e l'ora in una stringa nel formato desiderato

            # Esegui la query con i parametri della visita
            cursor.execute(query, (visita[0], visita[1], visita[3]))

            # Commit delle modifiche
            self.conn.commit()
            
            print("Visita eliminata con successo.")
        except mysql.connector.Error as err:
            print("Errore durante l'eliminazione della visita:", err)

    def eliminaVisitaM(self, visita):
        table_name = 'visitaMedico'
        cursor = self.conn.cursor()

        try:
            # Esegui la query per eliminare la visita
            query = f"DELETE FROM {table_name} WHERE CFPaziente = %s AND CFMedico = %s AND DataOra = %s"
            
            # Converti la stringa in un oggetto datetime
            #data_ora_str = visita[3][18:-1]  # Estrai la parte di stringa contenente la data e l'ora effettive
            #data_ora_datetime = datetime.strptime(data_ora_str, "%Y, %m, %d, %H, %M, %S")  # Converte la stringa in un oggetto datetime
            #data_ora_formattata = data_ora_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Formatta la data e l'ora in una stringa nel formato desiderato

            # Esegui la query con i parametri della visita
            cursor.execute(query, (visita[0], visita[1], visita[3]))

            # Commit delle modifiche
            self.conn.commit()
            
            print("Visita eliminata con successo.")
        except mysql.connector.Error as err:
            print("Errore durante l'eliminazione della visita:", err)


    @log_actions
    def ottieniMedici(self):
        table_name = 'medico'
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                result = cursor.fetchall()  # Ottieni tutte le righe risultanti dalla query
                return result
        except Exception as e:
            print("Si è verificato un errore durante l'ottenimento dei dati dal database:", e)
            return None  # Ritorna None in caso di errore

    @log_actions
    def addNuovoCurato(self, CFPaziente, CFMedico):
        self._sqlInjectionCheck(CFPaziente, CFMedico)
        # Nome della tabella in cui inserire i nuovi dati
        table_name = 'curato'
        cursor = self.conn.cursor()
        try:
            # Esegui una query per inserire i nuovi dati nella tabella paziente
            cursor.execute(f"INSERT INTO {table_name} (CFMedico, CFPaziente) VALUES (%s, %s)", (CFMedico, CFPaziente))
            # Conferma la transazione
            self.conn.commit()
            # Ottieni il numero di righe inserite
            num_rows_inserted = cursor.rowcount
            return num_rows_inserted
        except Exception as e:
            # Annulla eventuali modifiche in caso di errore
            self.conn.rollback()
            print("Si è verificato un errore durante l'inserimento dei dati nel database:", e)
            return 0
        finally:
            # Chiudi il cursore
            cursor.close()

    @log_actions
    def getVisitaOS(self, tupla):
        table_name = 'visitaOperatore'
        cursor = self.conn.cursor()
        try:
            query = f"SELECT * FROM {table_name} WHERE CFPaziente = %s AND CFOperatoreSanitario = %s AND DataOra = %s"
            cursor.execute(query, (tupla[0], tupla[1], tupla[3]))
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            print("Errore durante il recupero della visita:", err)
            return []
    
    @log_actions
    def addNuovoAuth(self, CF, Username, Password, Ruolo):
        table_name = 'autenticazione'
        cursor = self.conn.cursor()
        try:
            query = f"INSERT INTO autenticazione (CF, Username, Password, Ruolo) VALUES (AES_ENCRYPT(%s, '{self.key}'), AES_ENCRYPT(%s, '{self.key}'), AES_ENCRYPT(%s, '{self.key}'), AES_ENCRYPT(%s, '{self.key}'))"
            values = (CF, Username, Password, Ruolo)
            cursor.execute(query, values)
            self.conn.commit()
            print("Nuovo record aggiunto alla tabella 'autenticazione'.")
        except mysql.connector.Error as err:
            print("Errore durante l'aggiunta della nuova autenticazione:", err)
            return []
