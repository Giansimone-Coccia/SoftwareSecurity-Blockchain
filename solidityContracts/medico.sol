pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract Dottore {
    string nomePaziente;
    string pressione;
    string battito;
    string glicemia;
    string temperatura;
    string[] medicine;
    uint256 DataOraVisita;
    string luogo;

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
    
    mapping(address => mapping(string => Visita)) public dottore;

    function addMedicalRecord(string memory _nomePaziente, string memory _pressione, string memory _battito, string memory _glicemia, string memory _temperatura, string[] memory _medicine, uint256 _dataOraVisita, string memory _luogo) public {
        dottore[msg.sender][_nomePaziente] = Visita(_nomePaziente, _pressione, _battito, _glicemia, _temperatura, _medicine, _dataOraVisita, _luogo);
    }

    function addValues(string memory _battito, string memory _pressione) public {
        battito = _battito;
        pressione = _pressione;
    }

    function retrieve() public view returns (string memory, string memory, string memory, string memory, string memory, string[] memory, uint256, string memory) {
        return (nomePaziente, pressione, battito, glicemia, temperatura, medicine,DataOraVisita, luogo);
    }

}