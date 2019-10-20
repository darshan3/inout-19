import sys
import time
import pprint

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from solc import compile_source

def compile_source_file(file_path):
	with open(file_path, 'r') as f:
		source = f.read()

	return compile_source(source)

def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).deploy()

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address

w3 = Web3(EthereumTesterProvider())
contract_source_path = '../contracts/tradewars.sol'
compiled_sol = compile_source_file('../contracts/tradewars.sol')

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_contract(w3, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))

store_var_contract = w3.eth.contract(
   address=address,
   abi=contract_interface['abi'])

gas_estimate = store_var_contract.functions.setVar(255).estimateGas()
print("Gas estimate to transact with setVar: {0}\n".format(gas_estimate))

if gas_estimate < 100000:
  print("Sending transaction to setVar(255)\n")
  tx_hash = store_var_contract.functions.setVar(255).transact()
  receipt = w3.eth.waitForTransactionReceipt(tx_hash)
  print("Transaction receipt mined: \n")
  pprint.pprint(dict(receipt))
  print("Was transaction successful? \n")
  pprint.pprint(receipt['status'])
else:
  print("Gas cost exceeds 100000")