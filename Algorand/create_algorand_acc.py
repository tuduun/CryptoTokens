import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

# Write down the address, private key, and the passphrase for later usage
#generate_algorand_keypair()

def first_transaction_example(private_key, my_address):
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    receiver = "VLXIDAD6V2ZDBQAALAGVE277GBGXSBX22XKJJ4E7TW27COKFISUF45R5UM"
    amount = 0
    note = "253966"

    #create transaction using all of the parameters before 
    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")



# replace private_key and my_address with your private key and your address.



generate_algorand_keypair()
#first_transaction_example('ubZg9TMgKELH96SuWLVfV16J5vDlfgMGzStdGd4fybBEBDd8ykdg7iQmTJZqQn+h3wzC7wni/60HUOwPakAwDw==+W459NyVGu6SrfFmqIxgnrTnw==', 'IQCDO7GKI5QO4JBGJSLGUQT7UHPQZQXPBHRP7LIHKDWA62SAGAHXHCXWEA')



#My account 1:
'''
My address: IQCDO7GKI5QO4JBGJSLGUQT7UHPQZQXPBHRP7LIHKDWA62SAGAHXHCXWEA
My private key: ubZg9TMgKELH96SuWLVfV16J5vDlfgMGzStdGd4fybBEBDd8ykdg7iQmTJZqQn+h3wzC7wni/60HUOwPakAwDw==+W459NyVGu6SrfFmqIxgnrTnw==
My passphrase: strong lizard wide add expect spatial sail pilot beyond step quit tornado bargain defy convince leave scatter cross nominee noise rotate elevator main absent win
'''

#My account 2:

'''
My address: WLIMMTEEQUAGB6JYL2G2QB254JKTC32N2XRI754GQVHV2NEZZEYAKNUAKE
My private key: pXVpM4A/nCW4NIfH1E0HfUdCN8TzbrTSRiLntUP7qCey0MZMhIUAYPk4Xo2oB13iVTFvTdXij/eGhU9dNJnJMA==
My passphrase: regret place boost way debris annual place mango ocean dance lonely jelly loyal assist owner humble final brave muffin fury manual disagree diary ability cabbage
'''

#DUmmy account 3

'''
My address: AGNV6NBCXR3MI56S525AXCJNIQPFJUCWFYJUZPFKDZSHN65IBZL7IGUCWM
My private key: vOTKuXeQBLHKiwoaEJH9XoTnM4cX0A1dxg02rJGbFHcBm180Irx2xHfS7roLiS1EHlTQVi4TTLyqHmR2+6gOVw==
My passphrase: nurse clog table alter ankle proof furnace appear addict dust learn echo someone smooth rotate source payment bonus alone sell cash cheap reward about check

'''


'''

some mnemonic:
1. under
2. cost
3. pipe
4. void
5. glory
6. silver
7. visual
8. vacant
9. side
10. effort
11. rookie
12. coconut
13. elevator
14. wave
15. indicate
16. label
17. replace
18. capable
19. narrow
20. food
21. include
22. cliff
23. scene
24. absent
25. head

'''