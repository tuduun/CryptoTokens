import json
import hashlib
import os
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future.transaction import *
# CREATE ASSET
# Get network params for transactions before every transaction.
# Specify your node address and token. This must be updated.
# algod_address = ""  # ADD ADDRESS
# algod_token = ""  # ADD TOKEN

def setting_up_keys():
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    # Initialize an algod client
    algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)


    mnemonic1 = "strong lizard wide add expect spatial sail pilot beyond step quit tornado bargain defy convince leave scatter cross nominee noise rotate elevator main absent win"
    mnemonic2 = "regret place boost way debris annual place mango ocean dance lonely jelly loyal assist owner humble final brave muffin fury manual disagree diary ability cabbage"

    # never use mnemonics in production code, replace for demo purposes only

    # For ease of reference, add account public and private keys to
    # an accounts dict.
    accounts = {}
    counter = 1
    for m in [mnemonic1,mnemonic2]:
        accounts[counter] = {}
        accounts[counter]['pk'] = mnemonic.to_public_key(m)
        accounts[counter]['sk'] = mnemonic.to_private_key(m)
        counter += 1
    print("Account 1 address: {}".format(accounts[1]['pk']))
    print("Account 2 address: {}".format(accounts[2]['pk']))





#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

def create_fungible_asset():
    print("Account 1 address: {}".format(accounts[1]['pk']))
    params = algod_client.suggested_params()
    # params.fee = 1000
    # params.flat_fee = True
    # Account 1 creates an asset called latinum and
    # sets Account 2 as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction
    txn = AssetConfigTxn(
        sender=accounts[1]['pk'],
        sp=params,
        total=100000,
        default_frozen=False,
        unit_name="abcdefu",
        asset_name="abcdefu coin",
        manager=accounts[1]['pk'],
        reserve=accounts[1]['pk'],
        freeze=accounts[1]['pk'],
        clawback=accounts[1]['pk'],
        url="https://path/to/my/asset/details", 
        decimals=1)
    # Sign with secret key of creator
    stxn = txn.sign(accounts[1]['sk'])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
    except Exception as err:
        print(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)

def create_an_NFT_arc69():
      # JSON file
    params = algod_client.suggested_params()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open (dir_path + '/metadata_arc69.json', "r")
    
    # Reading from file
    metadataJSON = json.loads(f.read())
    metadataStr = json.dumps(metadataJSON)

    hash = hashlib.new("sha512_256")
    hash.update(b"arc0003/amj")
    hash.update(metadataStr.encode("utf-8"))
    json_metadata_hash = hash.digest()
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    # Account 1 creates an asset called latinum and
    # sets Account 2 as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction
    txn = AssetConfigTxn(
            strict_empty_address_check = False,
            sender=accounts[1]['pk'],
            sp=params,
            total=1,      
            default_frozen=False,
            unit_name="Tugi_car",
            asset_name="Tugi Fast Car@arc69",
            manager=accounts[1]['pk'],
            reserve="",
            freeze="",
            clawback="",
            url="shorturl.at/bnOWZ",
            metadata_hash=json_metadata_hash,
            decimals=0)       
    # Sign with secret key of creator
    stxn = txn.sign(accounts[1]['sk'])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
    except Exception as err:    
        print(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)

#setting_up_keys()
#create_fungible_asset()    
#create_an_NFT_arc69()
#FUngible token ID = 101100127
# print_created_asset(algod_client, 'IQCDO7GKI5QO4JBGJSLGUQT7UHPQZQXPBHRP7LIHKDWA62SAGAHXHCXWEA', 101270175)    

