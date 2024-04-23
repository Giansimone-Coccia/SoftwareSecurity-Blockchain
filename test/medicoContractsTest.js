const MedicoContract = artifacts.require("MedicoContract");

contract("MedicoContract", (accounts) => {
  let medicoContractInstance;

  before(async () => {
    medicoContractInstance = await MedicoContract.deployed();
  });

  it("should store and retrieve visita hash correctly", async () => {
    const medico = accounts[0];
    const paziente = accounts[1];
    const hashDati = "hashDatiVisita000000000000000000";

    await medicoContractInstance.storeHashVisita(medico, paziente, hashDati);
    const retrievedHashes = await medicoContractInstance.retrieveHashVisita(medico, paziente);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve cartella clinica hash correctly", async () => {
    const paziente = accounts[1];
    const hashDati = "12345678910111213141516171819202";

    await medicoContractInstance.storeHashCartellaClinica(paziente, hashDati);
    const retrievedHash = await medicoContractInstance.retrieveHashCartellaClinica(paziente);

    assert.equal(retrievedHash, hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve farmaco hash correctly", async () => {
    const paziente = accounts[1];
    const hashDati = "12345678910111213141516171819202";

    await medicoContractInstance.storeHashFarmaco(paziente, hashDati);
    const retrievedHashes = await medicoContractInstance.retrieveHashFarmaco(paziente);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve patologie hash correctly", async () => {
    const idCartellaClinica = "idCartellaClinica";
    const hashDati = "12345678910111213141516171819202";

    await medicoContractInstance.storeHashPatologie(idCartellaClinica, hashDati);
    const retrievedHashes = await medicoContractInstance.retrieveHashPatologie(idCartellaClinica);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });
});
