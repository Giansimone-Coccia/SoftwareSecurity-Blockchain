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

        my_address = "0x7010e602876c406d9D3427047Cc880d2C633C2B0"
        private_key = "0xa7febb0ba2ec09bfc0910c95ed01c9fba1604357a438ba574f9ae5eccfa15afb"

        return abi, bytecode, w3, chain_id, my_address, private_key