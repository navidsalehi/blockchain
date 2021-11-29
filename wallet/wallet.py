import hashlib
import random
import json


import blockchain
import transaction
import blockchain
from config import Config

class Wallet:
    """
    Blockchain wallet with create - recover and view wallet with private and public key
    """

    wallets = []

    def __init__(self):
        self.transactions = transaction.Transaction()
        self.blockchain = blockchain.BlockChain()

    def generate_private_key(self, seeds) -> str:
        """
        Generate private key
        """
        return hashlib.sha256(seeds.encode()).hexdigest()

    def generate_public_key(self, private_key) -> str:
        """
        Generate public key
        """
        return hashlib.sha256(private_key.encode()).hexdigest()

    def get_balance(self, address):
        """Get wallet balance"""
        # TODO rewirte to new balance system
        balance = 0
        for block in self.blockchain.chain:
            for transaction in block["transactions"]:
                if transaction["recipient"] == address:
                    balance += transaction["amount"]
                elif transaction["sender"] == address:
                    balance -= transaction["amount"]
        return balance

    def create_wallet(self):
        """
        Create a wallet and return the private and public key
        """
        seeds = []

        with open(Config().SEED_WORDS_FILE_NAME) as file:
            words = file.readlines()
            words = [line.rstrip() for line in words]

        for i in range(12):
            word = random.choice(words)
            seeds.append(word)

        seeds_string = json.dumps(seeds)

        private_key = self.generate_private_key(seeds_string)
        public_key = self.generate_public_key(private_key)

        wallet = {"address": public_key, "private_key": private_key,  "amount": 0}
        self.wallets.append(wallet)
        return {"wallet": wallet, "seeds": seeds}

    def recover_wallet(self, private_key): 
        """
        Recover a wallet from private key
        """
        seeds_string = json.dumps(private_key)

        private_key = self.generate_private_key(seeds_string)
        public_key = self.generate_public_key(private_key)

        wallet = {"address": public_key, "private_key": private_key}
        return {"wallet": wallet}

    def view_wallet(self, public_key):

        """
        View a wallet from public key
        """

        wallet = {
            "wallet": public_key,
            "amount": self.transactions.get_balance(public_key),
        }

        return wallet
