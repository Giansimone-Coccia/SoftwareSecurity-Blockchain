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
    def __init__(self, path_file):
        self._path_file = path_file


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

        my_address = "0x312A145c284977a47e9A1962f7e00cd7Cfd88c86"
        private_key = "0x6be67da5254d3f4cc7addf87ed58216af1860e0eb3c732eb52e4b5812a288ad5"

        return abi, bytecode, w3, chain_id, my_address, private_key