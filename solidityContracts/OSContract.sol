pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract OSContract {

    mapping(string => mapping(string => string[])) public visita;
    event Evento(address msg, string message);

        // Funzione per memorizzare un hash nella mappatura
    function storeHashVisita(string memory _codiceFiscaleMedico, string memory _codiceFiscalePaziente, string memory _hashDati) public {
        require(bytes(_hashDati).length == 32, "Hash non corretto");
        visita[_codiceFiscaleMedico][_codiceFiscalePaziente].push(_hashDati);
        emit Evento(msg.sender,"Hash visita Operatore sanitario correttamente salvato");
    }

    // Funzione per recuperare l'array di visite per una specifica coppia di codici fiscali medico e paziente
    function retrieveHashVisita(string memory _codiceFiscaleOS, string memory _codiceFiscalePaziente) public view returns (string[] memory) {
        return visita[_codiceFiscaleOS][_codiceFiscalePaziente];
    }
    
}
