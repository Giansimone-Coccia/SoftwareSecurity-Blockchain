import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"medico.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["medico.sol"]["medico"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["medico.sol"]["medico"]["metadata"]
)["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

my_address = "0x8DB4ae822Ce55fBd25b2C4764DA86303B8172Efe"
private_key = "0x71b618e619b4ae65b3bf0b693afd7550b4f6062b9f3d6b9e9553cd4967406cbc"

# Create the contract in Python
Medico = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
# Submit the transaction that deploys the contract
transaction = Medico.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
medico = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
nome_paziente = "Nome del Paziente"
pressione = "120/80 mmHg"
battito = "70 bpm"
glicemia = "100 mg/dL"
temperatura = "36.5 °C"
medicine = ["Medicina 1", "Medicina 2"]
data_ora_visita = 1643889600  # Unix timestamp per la data e l'ora della visita
luogo = "Nome dell'Ospedale"

# Invia la transazione per inserire i dati della visita medica
greeting_transaction = medico.functions.addMedicalRecord(
    nome_paziente, pressione, battito, glicemia, temperatura, medicine, data_ora_visita, luogo
).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)