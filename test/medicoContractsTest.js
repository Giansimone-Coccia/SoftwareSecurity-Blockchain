
const MedicoContract = artifacts.require("MedicoContract");

contract("MedicoContract", (accounts) => {
  let medicoContractInstance;
  console.log("ciao")

  before(async () => {
    console.log("Before function called");
    try {
        medicoContractInstance = await MedicoContract.deployed();
        console.log("MedicoContract deployed at:", medicoContractInstance.address);
  
        // Puoi inserire qui eventuali operazioni aggiuntive da eseguire dopo il deploy del contratto
      } catch (error) {
        console.error("Errore durante il deploy del contratto:", error);
      }
    await new Promise(resolve => setTimeout(resolve, 10000));
    console.log("After before function");
    });

  it("should store and retrieve visita hash correctly", async () => {
    const medico = accounts[0];
    const paziente = accounts[1];
    const hashDati = "hashDatiVisita";

    await medicoContractInstance.storeHashVisita(medico, paziente, hashDati);
    const retrievedHashes = await medicoContractInstance.retrieveHashVisita(medico, paziente);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve cartella clinica hash correctly", async () => {
    const paziente = accounts[1];
    const hashDati = "hashDatiCartellaClinica";

    await medicoContractInstance.storeHashCartellaClinica(paziente, hashDati);
    const retrievedHash = await medicoContractInstance.retrieveHashCartellaClinica(paziente);

    assert.equal(retrievedHash, hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve farmaco hash correctly", async () => {
    const paziente = accounts[1];
    const hashDati = "hashDatiFarmaco";

    await medicoContractInstance.storeHashFarmaco(paziente, hashDati);
    const retrievedHashes = await medicoContractInstance.retrieveHashFarmaco(paziente);

    assert.equal(retrievedHashes.length, 1, "Il numero di hash memorizzati non è corretto");
    assert.equal(retrievedHashes[0], hashDati, "L'hash recuperato non corrisponde all'hash memorizzato");
  });

  it("should store and retrieve patologie hash correctly", async () => {
    co