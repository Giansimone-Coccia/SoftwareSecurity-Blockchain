const OSContract = artifacts.require("OSContract");

contract("OSContract", (accounts) => {
  let osContractInstance;

  before(async () => {
    osContractInstance = await OSContract.deployed();
  });

  it("should store and retrieve visita hash correctly", async () => {
    const medico = accounts[0];
    const paziente = accounts[1];
    const hashDati = "hashDatiVisita";

    await osContractInstance.storeHashVisita(medico, paziente, hashDati);
    const retrievedHashes = await osContractInstance.retrieveHashVisita(medico, paziente);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });
});
