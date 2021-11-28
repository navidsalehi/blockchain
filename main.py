from fastapi import FastAPI
import transaction

app = FastAPI()

from blockchain import *
from transaction import *
from wallet import *
from config import Config

mint_address = "0x12320ddb5f3070666e11237561d2995f6dfb6192"
blockChain = BlockChain()
transactions = Transaction()
wallet = Wallet()
mempool = Mempool()


@app.get('/', name="Home page", tags=["Page"], status_code=200)
def index():
    pass


@app.get('/chain', name="Blockchain", tags=["Blockchain"], status_code=200)
def blockchain():
    return blockChain.chain

@app.post('/mine', name="Mine", tags=["Blockchain"], status_code=201)
def mine():
    last_block = blockChain.get_last_block()
    last_proof = last_block["proof"]

    proof = blockChain.proof_of_work(last_proof)
    transactions.create_transaction(
        sender=Config.MINING_SENDER,
        recipient=mint_address,
        amount=Config.MINING_REWARD,
        type="mint",
    )

    blockChain.create_block(proof, blockChain.hash_block(last_block))
    return {
        "message": "New block mined", 
        "index": blockChain.get_last_block()["index"], 
        "transactions": blockChain.get_last_block()["transactions"], 
        "proof": blockChain.get_last_block()["proof"], 
        }

@app.get('/wallets', name="Wallets list", tags=["Wallets"], status_code=200)
def wallets():
    return [wallet for wallet in wallet.wallets]
    
@app.post('/wallets', name="Create new wallet", tags=["Wallets"], status_code=201)
def create_wallet():
    """ Create new wallet with seeds """
    return wallet.create_wallet()
        
@app.get('/wallets/{address}', name="View wallet details", tags=["Wallets"], status_code=200)
def view_wallet(address: str):
    """ View wallet transactions and balance """
    wallet_transasctons = transactions.get_transactions_by_address(address)
    wallet_balance = wallet.get_balance(address)

    return {
        "address": address,
        "transactions": wallet_transasctons,
        "balance": wallet_balance
    }

        
@app.post('/transaction/new', name="Create transactions", tags=["transaction"], status_code=201)
def create_transaction(sender: str, recipient: str, amount: float):
    """ insert new transaction to mempool """
    transaction = mempool.insert_transaction(sender, recipient, amount)
    return transaction

        
@app.get('/transaction', name="View mempool transactions", tags=["transaction"], status_code=200)
def view_mempool():
    """ insert new transaction to mempool """
    return mempool.transactions

     