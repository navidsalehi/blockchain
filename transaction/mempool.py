import json 

from config import Config
from .balance import Balance


class Mempool:


    def __init__(self):
        self.balances = Balance()
        self.config = Config()
        self.transactions = []
        self.load_mempool()

    def insert_transaction(self, transaction):
        """
        Add a transaction to the mempool
        """

        if transaction["sender"] == None or transaction["recipient"] == None or transaction["amount"] == None:
            return False

        if transaction["sender"] != Config().MINING_REWARD_SENDER:
            if self.balances.get_balance(transaction["sender"]) < transaction["amount"]:
                return False

        self.load_mempool()
        
        self.transactions.append(transaction)
        
        self.persist_mempool()

        return True

    def persist_mempool(self):
        """
        Persist the mempool to a file
        """
        with open(Config.MEMPOOL_FILE_NAME, "w") as file:
            json.dump(self.transactions, file)
        

    def load_mempool(self):
        """
        Load the mempool from a file
        """
        with open(Config.MEMPOOL_FILE_NAME, "r") as file:
            if file:
                try:
                    self.transactions = json.load(file)
                except:
                    self.transactions = []
        file.close()


    def clear_mempool(self):
        """
        Clear the mempool
        """
        self.transactions = []
        self.persist_mempool()