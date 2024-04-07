
class IntegrityCheckError(Exception):
    """Eccezione personalizzata per gestire situazioni specifiche."""
    
    def __init__(self, messaggio):
        """Inizializzazione dell'eccezione con un messaggio specifico."""
        self.messaggio = messaggio
        super().__init__(self.messaggio)
