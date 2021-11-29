import hashlib
import random
import uuid

from blockchain import BlockChain
from config import Config
from .balance import Balance
from .mempool import Mempool


class Transaction:
    """Transaction manager new - list - detail"""

    balances = []

    def __init__(self):
        self.mempool = Mempool()
        self.blockchain = BlockChain()
        self.balances = Balance()

    def create_transaction(
        self, sender: str, recipient: str, amount: float, type: str
    ) -> bool:
        """Create a new transaction and update wallets balance"""
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_id = self.generate_transaction_id()
        self.fee = self.amount * 0.02
        self.nonce = uuid.uuid4().hex
        # TODO sign transaction

        if sender != Config().MINING_REWARD_SENDER:
            if self.balances.get_balance(sender) <= self.amount + self.fee:
                return False

        transaction = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "transaction_id": self.transaction_id,
            "fee": self.fee,
            "type": type,
            "nonce" : self.nonce
        }
        self.mempool.insert_transaction(transaction)
        return True

    def generate_transaction_id(self):
        """Generate a unique id for the transaction"""
        nonce = random.randint(10000000, 99999999)
        return hashlib.sha256(
            (
                str(nonce) + str(self.sender) + str(self.recipient) + str(self.amount)
            ).encode()
        ).hexdigest()

    def sign_transaction(self, private_key):
        """Sign the transaction with the private key"""
        self.signature = self.generate_signature(private_key)

    def generate_signature(self, private_key):
        """Generate a signature for the transaction"""
        return private_key.sign(self.transaction_id.encode())

    def verify_transaction(self):
        """Verify the signature of the transaction"""
        return self.sender.verify(self.signature, self.transaction_id.encode())

    def get_transactions_by_address(self, address):
        """Get all transactions by address"""
        transactions = []
        for block in self.blockchain.chain:
            for transaction in block["transactions"]:
                if transaction["sender"] == address:
                    transactions.append(transaction)

                elif transaction["recipient"] == address:
                    transactions.append(transaction)

        return transactions
