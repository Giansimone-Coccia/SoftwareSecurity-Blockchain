pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract OSContract {

    mapping(string => mapping(string => string[])) public visita;

        // Funzione per memorizzare un hash nella mappatura
    function storeHashVisita(string memory _codiceFiscaleOS, string memory _codiceFiscalePaziente, string memory _hashDati) public {
        visita[_codiceFiscaleOS][_codiceFiscalePaziente].push(_hashDati);
    }

    // Funzione per recuperare l'array di visite per una specifica coppia di codici fiscali medico e paziente
    function retrieveHashVisita(string memory _codiceFiscaleOS, string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return visita[_codiceFiscaleOS][_codiceFiscalePaziente];
    }
    
}
