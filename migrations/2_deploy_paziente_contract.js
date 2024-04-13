const PazienteContract = artifacts.require("PazienteContract");

module.exports = function (deployer) {
  deployer.deploy(PazienteContract);
};
