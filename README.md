# CareChain

<p align="center">
  <img src="Logo-progetto.jpg">
</p>


CareChain è un software che facilita la gestione e la condivisione dei dati tra pazienti, medici e operatori sanitari utilizzando la tecnologia blockchain. È progettato per fornire una base solida sulla quale gli utenti possono sviluppare il proprio operato e condividere informazioni sensibili in modo sicuro e trasparente.

## Funzionalità

- **Gestione dei dati**: Consentire agli utenti di archiviare e accedere ai propri dati medici in modo sicuro e affidabile.
- **Condivisione sicura**: Fornire un meccanismo per la condivisione selettiva dei dati tra pazienti, medici e operatori sanitari.
- **Trasparenza**: Utilizzare la blockchain per garantire la tracciabilità e l'immuatabilità delle transazioni di dati.
- **Interfaccia utente intuitiva**: Offrire un'esperienza utente semplice e intuitiva per facilitare l'utilizzo del software.

## Tecnologie utilizzate

- **Blockchain**: Utilizziamo la blockchain Ganache per garantire la sicurezza e l'integrità dei dati.
- **Python**: Il backend del software è sviluppato in Python per la sua flessibilità e facilità di sviluppo.
- **Interfaccia a linea di comando (CLI)**: Attualmente supportiamo un'interfaccia a linea di comando per l'interazione con il software.

## Installazione

***Affinché risulti possibile utilizzare il programma, è consigliato non utilizzare la rete UnivPM per testare il programma***

Per installare e utilizzare CareChain, segui questi passaggi:

1. Clona il repository sul tuo computer: ci sono vari modi per farlo
   - **git clone** https://github.com/Giansimone-Coccia/SoftwareSecurity-Blockchain.git nella repository di interesse
   - alternativamente, è possibile direttamente clonarlo attraverso l'utilizzo di GitHub Desktop
   - Scaricando direttamente il file .zip e aprirlo tramite un IDE appropriato come Visual Studio Code.

2. Posizionrsi nella directory del progetto tramite terminale

3. Installa le dipendenze necessarie attraverso il seguente comando
   
   - **pip** install -r requirements.txt
4. Modifica dell'indirizzo e della chiave privata

   Affinché risulti possibile utilizzare il programma correttamente con l'utilizzo della blockchain Ganache è necessario:
   - Aprire Ganache
   - Scegliere uno dei possibili profili messi a disposizione
   - Copiare e incollare l'indirizzo e la chiave privata, da Ganache, nel file Chiavi.env del progetto nei seguenti campi:
      - MY_ADDRESS="la_tua_chiave"
      - PRIVATE_KEY="la_tua_chiave_privata"
5. Avvia il software:
   - Semplicemente mandando in run il programma attraverso l'IDE Visual Studio Code
   - oppure posizionandosi nella directory corretta e, da terminale, attraverso la direttiva **python3** main.py

