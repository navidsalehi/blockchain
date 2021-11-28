import hashlib
import json
import random

from blockchain import BlockChain


class Transaction:
    """ Transaction manager new - list - detail """

    def __init__(self):
        self.blockchain = BlockChain()
    
    mempool = []

    def create_transaction(self, sender: str, recipient: str, amount: float, type: str):
        """ Create a new transaction """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_id = self.generate_transaction_id()
        self.fee = self.amount * 0.02
        #TODO sign transaction
        
        transaction = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "transaction_id": self.transaction_id,
            "fee": self.fee,
            "type" : type
        }
        self.mempool.append(transaction)

    def generate_transaction_id(self):
        """ Generate a unique id for the transaction """
        nonce = random.randint(10000000, 99999999)
        return hashlib.sha256((str(nonce) + str(self.sender) + str(self.recipient) + str(self.amount)).encode()).hexdigest()

    def sign_transaction(self, private_key):
        """ Sign the transaction with the private key """
        self.signature = self.generate_signature(private_key)

    def generate_signature(self, private_key):
        """ Generate a signature for the transaction """
        return private_key.sign(self.transaction_id.encode())

    def verify_transaction(self):
        """ Verify the signature of the transaction """
        return self.sender.verify(self.signature, self.transaction_id.encode())

    def get_transactions_by_address(self, address):
        """ Get all transactions by address """
        transactions = []
        for block in self.blockchain.chain:
            for transaction in block["transactions"]:
                if transaction["sender"] == address:
                    transactions.append(transaction)

                elif transaction["recipient"] == address:
                    transactions.append(transaction)

        return transactions