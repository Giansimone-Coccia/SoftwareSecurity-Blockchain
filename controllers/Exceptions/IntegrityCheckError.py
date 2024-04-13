

import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class IntegrityCheckError(Exception):
    """Eccezione personalizzata per gestire situazioni specifiche."""
    
    def __init__(self, messaggio):
        """Inizializzazione dell'eccezione con un messaggio specifico."""
        self.messaggio = messaggio
        logging.error(f"IntegrityCheckError: {messaggio}")
        super().__init__(self.messaggio)
