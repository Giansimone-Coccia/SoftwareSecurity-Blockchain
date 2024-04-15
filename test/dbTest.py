from faker import Faker

# Inizializza l'istanza di Faker
faker = Faker()

import unittest
from unittest.mock import MagicMock # Per evitare l'effettiva connessione al db
from database.db import db

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.database = db()
        self.db.conn = MagicMock()

    def tearDown(self):
        self.db.conn.close.assert_called_once()

    def test_ottieniDatiAuth(self):
        # Mock dei dati di esempio
        mock_data = [
            (faker.ssn(), faker.user_name(), faker.password(), faker.job()),
            (faker.ssn(), faker.user_name(), faker.password(), faker.job())
        ]
        
        # Mock del metodo di esecuzione della query
        self.db.conn.cursor().fetchall.return_value = mock_data
        
        result = self.db.ottieniDatiAuth()

        # Assert
        self.assertEqual(len(result), len(mock_data))


    def test_retrieve_data(self):
        # Verifica se i metodi di recupero dei dati restituiscono risultati corretti
        mock_data = [
            {'CF': '123456789', 'Username': 'user1', 'Password': 'password1', 'Ruolo': 'ruolo1'},
            {'CF': '987654321', 'Username': 'user2', 'Password': 'password2', 'Ruolo': 'ruolo2'}
        ]

        self.db.ottieniDatiAuth = MagicMock(return_value=mock_data)

        result = self.db.ottieniDatiAuth()
        self.assertEqual(result, mock_data)

    def test_modify_data(self):
        # Verifica se i metodi di aggiunta/modifica/eliminazione dei dati funzionano correttamente

        # Aggiunta di un nuovo paziente di mock
        num_rows_inserted = self.db.addNuovoPaziente('CF123', 'Nome', 'Cognome', 'Residenza')
        self.assertEqual(num_rows_inserted, 1)  # Verifica se è stata inserita una nuova riga

        # Modifica del dosaggio di un farmaco
        success = self.db.modificaDosaggiofarmaco('CF123', 'NomeFarmaco', 'NuovoDosaggio')
        self.assertTrue(success)  # Verifica se la modifica è avvenuta con successo

        # Eliminazione di una visita
        visita = ('CFPaziente', 'CFOperatoreSanitario', 'Altro', 'DataOra')
        self.db.eliminaVisitaOS = MagicMock() 
        self.db.eliminaVisitaOS(visita)
        self.db.eliminaVisitaOS.assert_called_once_with(visita)

    def test_exception_handling(self):
        # Verifica se le eccezioni vengono gestite correttamente

        # Simula un errore di connessione al database
        self.db.conn.close()  # Chiudi la connessione per simulare un errore di connessione
        with self.assertRaises(Exception):  # Verifica se viene sollevata un'eccezione
            self.db.ottieniDatiAuth()

if __name__ == '__main__':
    unittest.main()
