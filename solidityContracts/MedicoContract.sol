pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract MedicoContract {

    mapping(string => mapping(string => string[])) public visita;
    mapping(string => string) public cartellaClinica;
    mapping(string => string[]) public farmaco;
    mapping(string => string[]) public patologie;

    event Evento(address  _sender, string _message);


    // Funzione per memorizzare un hash nella mappatura
    function storeHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        visita[_codiceFiscaleMedico][_codiceFiscalePaziente].push(_hashDati);
        emit Evento(msg.sender,"Hash visita correttamente salvato");
    }

    // Funzione per recuperare l'array di visite per una specifica coppia di codici fiscali medico e paziente
    function retrieveHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return visita[_codiceFiscaleMedico][_codiceFiscalePaziente];
    }

    // Funzione per memorizzare un hash nella mappatura
    function storeHashCartellaClinica(string memory _codiceFiscalePaziente, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        cartellaClinica[_codiceFiscalePaziente] = _hashDati;
        emit Evento(msg.sender,"Hash cartella clinica correttamente salvato");
    }

    // Funzione per recuperare l'hash per un determinato codice fiscale del paziente
    function retrieveHashCartellaClinica(string memory _codiceFiscalePaziente) public view returns (string memory) {
        return cartellaClinica[_codiceFiscalePaziente];
    }

    // Funzione per aggiornare l'hash di una cartella clinica
    function modifyHashCartellaClinica(string memory _codiceFiscalePaziente, string memory _newHash) public {
        require(bytes(_newHash).length == 32, "Hash non corretto");
        cartellaClinica[_codiceFiscalePaziente] = _newHash;
        emit Evento(msg.sender,"Hash cartella clinica correttamente salvato");
    }

    // Funzione per memorizzare un farmaco nella mappatura
    function storeHashFarmaco(string memory _codiceFiscalePaziente, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        farmaco[_codiceFiscalePaziente].push(_hashDati);
        emit Evento(msg.sender,"Hash farmaco correttamente salvato");
    }

    // Funzione per recuperare un farmaco
    function retrieveHashFarmaco(string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return farmaco[_codiceFiscalePaziente];
    }

        // Funzione per memorizzare una patologia nella mappatura
    function storeHashPatologie(string memory _idCartellaClinica, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        patologie[_idCartellaClinica].push(_hashDati);
        emit Evento(msg.sender,"Hash patologia correttamente salvato");
    }

    // Funzione per recuperare una patologia
    function retrieveHashPatologie(string memory _idCartellaClinica) public view returns (string[] memory) {
        return patologie[_idCartellaClinica];
    }

    

}
