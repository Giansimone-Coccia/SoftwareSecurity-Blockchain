pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract Visita {

    mapping(string => mapping(string => string[])) public visita;

    // Funzione per memorizzare un hash nella mappatura
    function storeHash(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente, string memory _hashDati) public {
        visita[_codiceFiscaleMedico][_codiceFiscalePaziente].push(_hashDati);
    }

    // Funzione per recuperare l'array di visite per una specifica coppia di codici fiscali medico e paziente
    function retrieveHash(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return visita[_codiceFiscaleMedico][_codiceFiscalePaziente];
    }
}
