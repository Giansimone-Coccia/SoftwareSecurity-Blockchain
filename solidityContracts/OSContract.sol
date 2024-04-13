pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract OSContract {

    mapping(string => string) public cartellaClinica;

    // Funzione per memorizzare un hash nella mappatura
    function storeHashCartellaClinica(string memory _codiceFiscalePaziente, string memory _hashDati) public {
        cartellaClinica[_codiceFiscalePaziente] = _hashDati;
    }

    // Funzione per recuperare l'hash per un determinato codice fiscale del paziente
    function retrieveHashCartellaClinica(string memory _codiceFiscalePaziente) public view returns (string memory) {
        return cartellaClinica[_codiceFiscalePaziente];
    }
    
}
