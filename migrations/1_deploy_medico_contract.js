const MedicoContract = artifacts.require("MedicoContract");

module.exports = function(deployer) {
  deployer.deploy(MedicoContract);
};
