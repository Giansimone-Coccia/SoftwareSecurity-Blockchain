const OSContract = artifacts.require("OSContract");

module.exports = function (deployer) {
  deployer.deploy(OSContract);
};
