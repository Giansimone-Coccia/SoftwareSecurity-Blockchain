pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract PazienteContract {

    mapping(string => string[]) public cartellaClinica;
    mapping(string => mapping(string => string[])) public visita;


    // Funzione per memorizzare un hash nella mappatura
    function storeHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente, string memory _hashDati) public {
        visita[_codiceFiscaleMedico][_codiceFiscalePaziente].push(_hashDati);
    }

    // Funzione per recuperare l'hash per un determinato codice fiscale del paziente
    function retrieveHashCartellaClinica(string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return cartellaClinica[_codiceFiscalePaziente];
    }

    // Funzione per recuperare l'array di visite per una specifica coppia di codici fiscali medico e paziente
    function retrieveHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return visita[_codiceFiscaleMedico][_codiceFiscalePaziente];
    }
    
}
