from faker import Faker
import unittest
from unittest.mock import MagicMock
from database.db import db
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Inizializzazione delle risorse specifiche del test prima di eseguire ogni singolo test
        self.database = db()  # Assicurati che db() sia la classe che gestisce la connessione al database
        self.database.conn = MagicMock()  # Mock della connessione al database
        self.cursor = self.database.conn.cursor()  # Ottenimento del cursore per il test
        self.cursor.rowcount = MagicMock(return_value=1)
        self.faker = Faker()  # Utilizzo di Faker per generare dati di test
        self.key = '2b7e151628aed2a6'.encode('utf-8')
        # Creazione di un cifrario AES con la chiave
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def tearDown(self):
        self.cursor.close()  # Chiusura del cursore
        try:
            self.database.conn.close()  # Chiusura della connessione al database
        except AttributeError:
            pass  # Ignora se la connessione non è stata impostata


    def test_retrieve_data(self):
        mock_data = [
            {'CF': '123456789', 'Username': 'user1', 'Password': 'password1', 'Ruolo': 'ruolo1'},
            {'CF': '987654321', 'Username': 'user2', 'Password': 'password2', 'Ruolo': 'ruolo2'}
        ]

        self.database.ottieniDatiAuth = MagicMock(return_value=mock_data)

        result = self.database.ottieniDatiAuth(self.cursor)
        self.assertEqual(result, mock_data)


    def test_modify_data(self):
        # Test aggiunta nuovo paziente
        cf = self.faker.ssn()
        nome = self.faker.first_name()
        cognome = self.faker.last_name()
        residenza = self.faker.city()

        # Mock della connessione e del cursore per l'aggiunta del nuovo paziente
        mock_cursor_add = MagicMock()
        mock_cursor_add.execute.return_value.rowcount = 1

        # Configurazione del side_effect per creare un nuovo oggetto mock ogni volta che viene chiamato il cursore, altrimenti
        # mock_add e mock_mod hanno lo stesso id e sembra che execute venga chiamato due volte
        self.database.conn.cursor.side_effect = lambda: mock_cursor_add

        # Esegui l'aggiunta del nuovo paziente
        self.database.addNuovoPaziente(cf, nome, cognome, residenza)

        # Verifica che l'aggiunta del nuovo paziente avvenga correttamente
        mock_cursor_add.execute.assert_called_once()  # Assicura che il metodo execute sia stato chiamato esattamente una volta

        # Test modifica dosaggio farmaco
        cf_paziente_modifica = self.faker.ssn()
        nome_farmaco = self.faker.word()
        dosaggio = self.faker.random_number()

        # Mock della connessione e del cursore per la modifica del dosaggio del farmaco
        mock_cursor_mod = MagicMock()
        mock_cursor_mod.execute.return_value.rowcount = 1

        # Configurazione del side_effect per creare un nuovo oggetto mock ogni volta che viene chiamato il cursore
        self.database.conn.cursor.side_effect = lambda: mock_cursor_mod
        mock_cursor_mod.execute.return_value = mock_cursor_mod
        mock_cursor_mod.execute.return_value.rowcount = 1

        # Esegui la modifica del dosaggio del farmaco
        self.database.modificaDosaggiofarmaco(cf_paziente_modifica, nome_farmaco, dosaggio)

        # Verifica che la modifica del dosaggio del farmaco avvenga correttamente
        mock_cursor_mod.execute.assert_called_once()  # Assicura che il metodo execute sia stato chiamato esattamente una volta


    def test_exception_handling(self):
        # Simula un errore di connessione al database
        self.database.conn.cursor.side_effect = Exception("Errore di connessione al database")

        # Verifica che il metodo sollevi correttamente un'eccezione quando si verifica un errore di connessione
        with self.assertRaises(Exception):
            self.database.ottieniDatiAuth(self.cursor)

        # Resetta il comportamento del mock per il successivo test
        self.database.conn.cursor.side_effect = None

        # Simula un'eccezione durante l'esecuzione della query
        self.database.conn.cursor.return_value.execute.side_effect = Exception("Errore durante l'esecuzione della query")

        # Verifica che il metodo sollevi correttamente un'eccezione quando si verifica un errore durante l'esecuzione della query
        with self.assertRaises(Exception):
            self.database.ottieniDatiAuth(self.cursor)


if __name__ == '__main__':
    unittest.main()
