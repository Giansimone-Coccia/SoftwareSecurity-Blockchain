pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract PazienteContract {

    mapping(string => string) public cartellaClinica;
    mapping(string => mapping(string => string[])) public visita;
    mapping(string => string[]) public farmaco;
    event Evento(address msg, string message);

    // Funzione per memorizzare un hash nella mappatura
    function storeHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        visita[_codiceFiscaleMedico][_codiceFiscalePaziente].push(_hashDati);
        emit Evento(msg.sender,"Hash correttamente salvato");
    }

    // Funzione per memorizzare un hash nella mappatura
    function storeHashCartellaClinica(string memory _codiceFiscalePaziente, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        cartellaClinica[_codiceFiscalePaziente] = _hashDati;
        emit Evento(msg.sender,"Hash cartella clinica correttamente memorizzata");
    }

    // Funzione per recuperare l'hash per un determinato codice fiscale del paziente
    function retrieveHashCartellaClinica(string memory _codiceFiscalePaziente) public view returns (string memory) {
        return cartellaClinica[_codiceFiscalePaziente];
    }

    // Funzione per recuperare l'array di visite per una specifica coppia di codici fiscali medico e paziente
    function retrieveHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return visita[_codiceFiscaleMedico][_codiceFiscalePaziente];
    }

    // Funzione per memorizzare un farmaco nella mappatura
    function storeHashFarmaco(string memory _codiceFiscalePaziente, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        farmaco[_codiceFiscalePaziente].push(_hashDati);
        emit Evento(msg.sender,"Hash farmaco correttamente memorizzato");
    }

    // Funzione per recuperare un farmaco
    function retrieveHashFarmaco(string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return farmaco[_codiceFiscalePaziente];
    }
    
}
