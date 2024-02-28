import logging
from web3 import Web3, HTTPProvider
from solcx import compile_source

# Set up the web3 provider
web3 = Web3(HTTPProvider('HTTP://127.0.0.1:7545'))

if web3.isConnected():
    # Set up the contract and account information
    account = web3.eth.accounts[0]
    contract_file = 'Dottore.sol'
    with open(contract_file) as f:
        contract_source_code = f.read()

    compiled_contract = compile_source(contract_source_code)
    contract_interface = compiled_contract['<stdin>:Dottore']
    contract_abi = contract_interface['abi']
    contract_bytecode = contract_interface['bin']

    # Deploy the contract
    contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    nome_paziente = "Nome del Paziente"
    pressione = "120/80 mmHg"
    battito = "70 bpm"
    glicemia = "100 mg/dL"
    temperatura = "36.5 °C"
    medicine = ["Medicina 1", "Medicina 2"]
    data_ora_visita = 1643889600  # Unix timestamp per la data e l'ora della visita
    luogo = "Nome dell'Ospedale"

    # Invia la transazione per inserire i dati della visita medica
    tx_hash = contract.functions.addMedicalRecord(
        nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo
    ).transact({'from': account, 'gas': web3.eth.gas_price})
    # Attendere la conferma della transazione
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Write contract address to a file
    with open('contract_address.txt', 'w') as f:
        f.write(receipt['contractAddress'])

    print('Dottore contract is now deployed at address ' + receipt['contractAddress'] + '.')
else:
    print('Unable to connect to the Ethereum client.')