pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract MedicoContract {

    mapping(string => mapping(string => string[])) public visita;
    mapping(string => string) public cartellaClinica;
    mapping(string => string) public farmaco;

    // Funzione per memorizzare un hash nella mappatura
    function storeHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente, string memory _hashDati) public {
        visita[_codiceFiscaleMedico][_codiceFiscalePaziente].push(_hashDati);
    }

    // Funzione per recuperare l'array di visite per una specifica coppia di codici fiscali medico e paziente
    function retrieveHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return visita[_codiceFiscaleMedico][_codiceFiscalePaziente];
    }

    // Funzione per memorizzare un hash nella mappatura
    function storeHashCartellaClinica(string memory _codiceFiscalePaziente, string memory _hashDati) public {
        cartellaClinica[_codiceFiscalePaziente] = _hashDati;
    }

    // Funzione per recuperare l'hash per un determinato codice fiscale del paziente
    function retrieveHashCartellaClinica(string memory _codiceFiscalePaziente) public view returns (string memory) {
        return cartellaClinica[_codiceFiscalePaziente];
    }

    // Funzione per aggiornare l'hash di una cartella clinica
    function modifyHashCartellaClinica(string memory _codiceFiscalePaziente, string memory _newHash) public {
        cartellaClinica[_codiceFiscalePaziente] = _newHash;
    }

    // Funzione per memorizzare un farmaco nella mappatura
    function storeHashFarmaco(string memory _codiceFiscalePaziente, string memory _hashDati) public {
        farmaco[_codiceFiscalePaziente] = _hashDati;
    }

    // Funzione per recuperare un farmaco
    function retrieveHashFarmaco(string memory _codiceFiscalePaziente) public view returns (string memory) {
        return farmaco[_codiceFiscalePaziente];
    }
}
