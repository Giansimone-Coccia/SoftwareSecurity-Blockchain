// SPDX-License-Identifier: MIT 
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract Medico {
    struct Visita {
        string nomePaziente;
        string pressione;
        string battito;
        string glicemia;
        string temperatura;
        string[] medicine;
        string dataOraVisita;
        string luogo;
    }
    
    mapping(address => mapping(string => Visita)) public medico;
    

    function addMedicalRecord(string memory _nomePaziente, string memory _pressione, string memory _battito, string memory _glicemia, string memory _temperatura, string[] memory _medicine, string memory  _dataOraVisita, string memory _luogo) public {
        Visita memory newVisit = Visita(_nomePaziente, _pressione, _battito, _glicemia, _temperatura, _medicine, _dataOraVisita, _luogo);
        medico[msg.sender][_nomePaziente] = newVisit;
    }

    function retrieve() public view returns (string memory, string memory, string memory, string memory, string memory, string[] memory, string memory, string memory) {
        Visita memory currentVisit = medico[msg.sender]["current"];
        return (currentVisit.nomePaziente, currentVisit.pressione, currentVisit.battito, currentVisit.glicemia, currentVisit.temperatura, currentVisit.medicine, currentVisit.dataOraVisita, currentVisit.luogo);
    }

    function getMedicalRecord(address _medico, string memory _nomePaziente) public view returns (string memory, string memory, string memory, string memory, string memory, string[] memory, string memory , string memory) {
        Visita memory visita = medico[_medico][_nomePaziente];
        return (
            visita.nomePaziente,
            visita.pressione,
            visita.battito,
            visita.glicemia,
            visita.temperatura,
            visita.medicine,
            visita.dataOraVisita,
            visita.luogo
        );
    }


    function getAllVisiteMedico() public view returns (Visita[] memory) {
        return visiteMedico[msg.sender];
    }

}


/* contract Medico {
    string nomePaziente;
    string pressione;
    string battito;
    string glicemia;
    string temperatura;
    string[] medicine;
    uint256 dataOraVisita;
    string luogo;

    struct Visita {
        string nomePaziente;
        string pressione;
        string battito;
        string glicemia;
        string temperatura;
        string[] medicine;
        uint256 dataOraVisita;
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
        return (nomePaziente, pressione, battito, glicemia, temperatura, medicine, dataOraVisita, luogo);
    }


    function getMedicalRecord(address _medico, string memory _nomePaziente) public view returns (string memory, string memory, string memory, string memory, string memory, string[] memory, uint256 , string memory) {
        Visita memory visita = dottore[_medico][_nomePaziente];
        return (
            visita.nomePaziente,
            visita.pressione,
            visita.battito,
            visita.glicemia,
            visita.temperatura,
            visita.medicine,
            visita.dataOraVisita,
            visita.luogo
        );
    }


} */