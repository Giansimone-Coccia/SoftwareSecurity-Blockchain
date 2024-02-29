pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

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
    
    mapping(address => mapping(string => Visita)) public dottore;

    function addMedicalRecord(string memory _nomePaziente, string memory _pressione, string memory _battito, string memory _glicemia, string memory _temperatura, string[] memory _medicine, uint256 _dataOraVisita, string memory _luogo) public {
        dottore[msg.sender][_nomePaziente] = Visita(_nomePaziente, _pressione, _battito, _glicemia, _temperatura, _medicine, _dataOraVisita, _luogo);
    }

    function returnData(string memory _nomePaziente) public view returns (string memory, string memory, string memory, string memory, string memory, string[] memory, uint256, string memory) {
        Visita memory visita = dottore[msg.sender][_nomePaziente];
        return (visita.nomePaziente, visita.pressione, visita.battito, visita.glicemia, visita.temperatura, visita.medicine, visita.DataOraVisita, visita.luogo);
    }
}