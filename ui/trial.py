import sys
import time
import pprint
import json
import pdb
# from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3, HTTPProvider
from solc import compile_source

# def compile_source_file(file_path):
# 	with open(file_path, 'r') as f:
# 		source = f.read()

# 	return compile_source(source)

# def deploy_contract(w3, contract_interface):
#     tx_hash = w3.eth.contract(
#         abi=contract_interface['abi'],
#         bytecode=contract_interface['bytecode']).deploy()

#     address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
#     return address

w3 = Web3(HTTPProvider('http://localhost:8545'))
# w3 = Web3(Web3.EthereumTesterProvider())
print(w3.isConnected())

with open('TradeWars.json') as f:
  ABI = json.load(f)

addr = "0xe1F73982eD697f41Ac6CDCB8421098B3dd011019"
twinst = w3.eth.contract(address=addr, abi=ABI)


account1 = "0x14b6f74d70931DFF8fBc33bbAEc6608D14E70949"
account2 = "0xf98AE10Df6ea8946B02D5EA8d404971a8F614356"
print(w3.eth.getBalance(account1))
print(w3.eth.getBalance(account2))
card = twinst.functions.addCard("Card1", "blank.png", 100,100).transact({"from":account1})
# pdb.set_trace()
card = twinst.functions.addCard("Card3", "blank.png", 300,300).transact({"from":account1})

card = twinst.functions.addCard("Card5", "blank.png", 500,500).transact({"from":account1})

card = twinst.functions.addCard("Card2", "blank.png", 200,200).transact({"from":account2})

card = twinst.functions.addCard("Card4", "blank.png", 400,400).transact({"from":account2})

card = twinst.functions.addCard("Card6", "blank.png", 600,600).transact({"from":account2})

# twinst.functions.addCard("Card1", "Im1", 100,100).transact({"from":account1})
# twinst.cards(card).call()


# twinst.
# with open('../build/contracts/TradeWars.json') as f:
#   contract_interface = json.load(f)
# pdb.set_trace()
# address = deploy_contract(w3, contract_interface)
# print("Deployed {0} to: {1}\n".format(contract_id, address))

pdb.set_trace()
# store_var_contract = w3.eth.contract(
#    address=address,
#    abi=contract_interface['abi'])

# gas_estimate = store_var_contract.functions.setVar(255).estimateGas()
# print("Gas estimate to transact with setVar: {0}\n".format(gas_estimate))

# if gas_estimate < 100000:
#   print("Sending transaction to setVar(255)\n")
#   tx_hash = store_var_contract.functions.setVar(255).transact()
#   receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#   print("Transaction receipt mined: \n")
#   pprint.pprint(dict(receipt))
#   print("Was transaction successful? \n")
#   pprint.pprint(receipt['status'])
# else:
#   print("Gas cost exceeds 100000")