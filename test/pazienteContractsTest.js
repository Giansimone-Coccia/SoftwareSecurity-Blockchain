const PazienteContract = artifacts.require("PazienteContract");

contract("PazienteContract", (accounts) => {
  let pazienteContractInstance;

  before(async () => {
    pazienteContractInstance = await PazienteContract.deployed();
  });

  it("should store and retrieve cartella clinica hash correctly", async () => {
    const paziente = accounts[0];
    const hashDati = "12345678910111213141516171819202";

    await pazienteContractInstance.storeHashCartellaClinica(paziente, hashDati);
    const retrievedHash = await pazienteContractInstance.retrieveHashCartellaClinica(paziente);

    assert.equal(retrievedHash, hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve visita hash correctly", async () => {
    const medico = accounts[1];
    const paziente = accounts[0];
    const hashDati = "12345678910111213141516171819202";

    await pazienteContractInstance.storeHashVisita(medico, paziente, hashDati);
    const retrievedHashes = await pazienteContractInstance.retrieveHashVisita(medico, paziente);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve farmaco hash correctly", async () => {
    const paziente = accounts[0];
    const hashDati = "12345678910111213141516171819202";

    await pazienteContractInstance.storeHashFarmaco(paziente, hashDati);
    const retrievedHashes = await pazienteContractInstance.retrieveHashFarmaco(paziente);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });
});
