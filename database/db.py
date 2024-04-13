
import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class db:

    def __init__(self):
        # Parametri di connessione al database
        config = {
            'user': 'progettoss',
            'password': 'Blockchain@!456',
            'host': 'db4free.net',
            'database': 'softwaresecurity',
            'port': '3306',
            'raise_on_warnings': True  # Opzionale, solleva un'eccezione su avvisi MySQL
        }

        self.key = 'Lvs5RZsgOSmB7y5R5lF1v5xFy5Z9S0Xr' # Chiave da usare anche nel db 

        try:
            # Connessione al database
            self.conn = mysql.connector.connect(**config)
              

        except mysql.connector.Error as err:
            print("Errore di connessione al database:", err)

        finally:
            # Chiudi la connessione
            if 'conn' in locals() and self.conn.is_connected():
                self.conn.close()
    
    def ottieniDatiAuth(self):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'autenticazione'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT AES_DECRYPT(CF,'{self.key}'), AES_DECRYPT(Username,'{self.key}'), AES_DECRYPT(Password,'{self.key}'), AES_DECRYPT(Ruolo,'{self.key}') FROM {table_name}")
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
    
    def ottieniAssistiti(self):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'assistito'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name}")
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    def ottieniCartelle(self):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'cartellaClinica'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name}")
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    def ottieniCartellaFromCF(self,cf):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'cartellaClinica'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = '{cf}'")
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows[0]
    
    def ottieniVisiteMedico(self, CFPaziente, CFMedico):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'visitaMedico'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = %s AND CFMedico = %s", (CFPaziente, CFMedico))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    def ottieniVisisteOS(self, CFPaziente, CFOperatore):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'visitaOperatore'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE CFPaziente = %s AND CFOperatoreSanitario = %s", (CFPaziente, CFOperatore))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows

    def ottieniFarmaci(self, CF):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'farmaci'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE IdCartellaClinica = %s", (CF,))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    def ottieniFarmaco(self, CF, nomeFarmaco):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'farmaci'
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE IdCartellaClinica = %s AND NomeFarmaco = %s", (CF, nomeFarmaco))
        # Recupera tutte le tuple
        rows = cursor.fetchall()
        return rows
    
    def modificaDosaggiofarmaco(self, CF, nomeFarmaco, dosaggio):
        try:
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
    
    def modificaStatoPatologia(self, CF, nomePatologia, stato):
        try:
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

    
    def ottieniPatologie(self, CF):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = 'patologie'
    
        cursor = self.conn.cursor()
        # Esegui una query per selezionare tutti i dati dalla tabella specificata
        cursor.execute(f"SELECT * FROM {table_name} WHERE IdCartellaClinica = %s", (CF,))

        # Recupera tutte le tuple
        rows = cursor.fetchall()

        return rows
    
    def ottieniDatiUtente(self, nomeTabella, CF):
        # Nome della tabella da cui desideri recuperare i dati
        table_name = nomeTabella
        cursor = self.conn.cursor()
        # Esegui una query per selezionare solo le righe con il CF specificato
        cursor.execute(f"SELECT * FROM {table_name} WHERE CF = %s", (CF,))
        # Recupera le righe filtrate
        rows = cursor.fetchall()
        return rows
    
    # def ottieniDatiVisite(self, CFMedico):
    #     # Nome della tabella da cui desideri recuperare i dati
    #     table_name = 'caretllaClinica'
    #     cursor = self.conn.cursor()
    #     # Esegui una query per selezionare solo le righe con il CF specificato
    #     cursor.execute(f"SELECT * FROM {table_name} WHERE CF = %s", (CF,))
    #     # Recupera le righe filtrate
    #     rows = cursor.fetchall()
    #     return rows

    def gestisciAccesso(self,username,password):
        utenti = self.ottieniDatiAuth()
        for u in utenti:
              if(u['Username']==username and u['Password']==password):
                  return True
        
        return False
    
    def ottieniProfessione(self,username,password):
         utenti = self.ottieniDatiAuth()

         for utente in utenti:
              if(utente['Username'] == username and utente['Password'] == password):
                return utente['Ruolo']
    
    def ottieniCF(self,username,password):
         utenti = self.ottieniDatiAuth()

         for utente in utenti:
              if(utente['Username'] == username and utente['Password'] == password):
                return utente['CF']

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


    def fromValueToId(self, nomeTabella, input_value):
        try:
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
    
    def updateCartellaClinica(self, CF, nuovo_trattamento):
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

