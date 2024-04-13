  module.exports = {
    contracts_directory: "./solidityContracts",
    contracts_build_directory: "./build/contracts", // Cartella in cui vengono salvati i contratti compilati
    networks: {
      development: {
        host: "127.0.0.1",     // Localhost (default: none)
        port: 7545,            // Porta predefinita di Ethereum (default: none)
        network_id: "*",       // Qualsiasi network (default: none)
      },
      // Puoi aggiungere altre reti qui, ad esempio reti di testnet o mainnet
    },
    compilers: {
      solc: {
        version: "0.6.0",    // Versione del compilatore Solidity da utilizzare
        settings: {
          optimizer: {
            enabled: false,   // Abilita l'ottimizzazione dei contratti (default: false)
            runs: 200,        // Numero di iterazioni per l'ottimizzazione (default: 200)
          },
        },
      },
    },
  };
  