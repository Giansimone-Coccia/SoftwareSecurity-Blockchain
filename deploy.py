import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

load_dotenv()

class Deploy:
    def __init__(self, file_name):
        self._file_name = file_name
        self._path_file = os.path.join(os.getcwd(), "solidityContracts", file_name)


    def create_contract(self):

        with open(self._path_file, "r") as file:
            simple_storage_file = file.read()

        # We add these two lines that we forgot from the video!
        print("Installing...")
        install_solc("0.6.0")

        file_name = os.path.basename(self._path_file)
        contract_name = file_name.split('.')[0]
        # Solidity source code
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {file_name: {"content": simple_storage_file}},
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
        bytecode = compiled_sol["contracts"][file_name][contract_name]["evm"][
            "bytecode"
        ]["object"]

        # get abi
        abi = json.loads(
            compiled_sol["contracts"][file_name][contract_name]["metadata"]
        )["output"]["abi"]

        w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
        chain_id = 1337

        my_address = "0xCB0A1451453024f5197D13E8db09e7f332e299Ae"
        private_key = "0xf048953f59a7310884282aa1a1567ca44bdb82d4c17897508f77b33e63f9f012"

        return abi, bytecode, w3, chain_id, my_address, private_key