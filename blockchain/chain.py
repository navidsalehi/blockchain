import hashlib
import json
from time import time


from transaction.mempool import Mempool
from config import Config
from transaction.balance import Balance
class BlockChain:
    """ Simple blockchain class """
    

    def __init__(self):
        """ Load chains form file or create genesis block"""
        
        self.mempool = Mempool()
        

        self.get_previous_blocks()
        if len(self.chain) <= 0:
            print("is less than one")
            self.create_block(previous_hash=1, proof=100)


    def create_block(self, proof: int, previous_hash=None):
        """ Create a new block """
        self.mempool.load_mempool()
        self.balances = Balance()
        aggreed_transactions = []


        for transaction in self.mempool.transactions:
            if transaction["sender"] != Config().MINING_REWARD_SENDER:

                if self.balances.get_balance(transaction["sender"]) >= (transaction["amount"]):
                    aggreed_transactions.append(transaction)
                    self.balances.update_balance(transaction["sender"], transaction["recipient"], transaction["amount"], transaction["fee"]) #TODO rewrite to better solution
            else:

                aggreed_transactions.append(transaction)
                self.balances.update_balance(transaction["sender"], transaction["recipient"], transaction["amount"], transaction["fee"]) #TODO rewrite to better solution

    
        block = {
            "index": len(self.chain) + 1,
            "timestamp": int(time()),
            "transactions": self.mempool.transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }
        self.chain.append(block)
        self.persist_chain()
        self.mempool.clear_mempool()
        return block



    def hash_block(self, block):
        """ Hash a block """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def verify_block(self, block, hash: str):
        """ Verify a block """
        pass

    def get_chain(self):
        """ Get the chain """
        pass

    def get_last_block(self):
        """ Get the last block """
        return self.chain[-1]

    def get_last_block_hash(self) -> str:
        """ Get the last block hash """
        pass

    def get_previous_blocks(self):
        """ Read persists blocks """
        with open(Config.BLOCKS_FILE_NAME, "r") as file:
            if file:
                try:
                    self.chain = json.load(file)
                except:
                    self.chain = []
        file.close()

    def persist_chain(self):
        """ Persist chain as json to file """
        with open(Config.BLOCKS_FILE_NAME, "w") as file:
            json.dump(self.chain, file)
        file.close()

    def valid_proof(self, last_proof, proof):
        """ Validate a proof """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[-4:] == "0000"


    def proof_of_work(self, last_proof):
        """ Simple proof of work algorithm """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof