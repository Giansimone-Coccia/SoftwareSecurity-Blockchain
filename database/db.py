
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

    
    def ottieniDati(self):
         # Nome della tabella da cui desideri recuperare i dati
            table_name = 'Utenti'
    
            cursor = self.conn.cursor()
            # Esegui una query per selezionare tutti i dati dalla tabella specificata
            cursor.execute(f"SELECT AES_DECRYPT(professione,'{self.key}'), AES_DECRYPT(email,'{self.key}'), AES_DECRYPT(password,'{self.key}') FROM {table_name}")

            # Recupera tutte le tuple
            rows = cursor.fetchall()

            # Stampa i valori decodificati per ogni tupla
            utenti = []
            for tupla in rows:
                tuplaDict = {'Professione':tupla[0].decode('utf-8'), 'Email':tupla[1].decode('utf-8'),
                             'Password':tupla[2].decode('utf-8')}
                utenti.append(tuplaDict)
            
            return utenti
    
    def gestisciAccesso(self,email,password):
        utenti = self.ottieniDati()
        for u in utenti:
              if(u['Email']==email and u['Password']==password):
                  return True
        
        return False
    

    def ottieniProfessione(self,email,password):
         utenti = self.ottieniDati()

         for utente in utenti:
              if(utente['Email'] == email and utente['Password'] == password):
                return utente['Professione']
        
    

                  
         

          
         
    


            
        



        
        
