pragma solidity ^0.8.0;

contract Dottore {
    struct Visita {
        string nomePaziente;
        string pressione;
        string battito;
        string glicemia;
        string temperatura;
        string[] medicine;
        uint256 DataOraVisita;
        string luogo;
    }
    
    mapping(address => mapping(string => Visita)) public Dottore;

    function addMedicalRecord(string memory _nomePaziente, string memory _pressione, string memory _battito, string memory _glicemia, string memory _temperatura, string[] memory _medicine, uint256 _dataOraVisita, string memory _luogo) public {
        Dottore[msg.sender][_nomePaziente] = Visita(_nomePaziente, _pressione, _battito, _glicemia, _temperatura, _medicine, _dataOraVisita, _luogo);
    }
}