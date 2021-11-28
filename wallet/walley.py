import os 
import hashlib

from blockchain import Blockchain
from transaction import Transaction

class Wallet:
    """ 
    Blockchain wallet with create - recover and view wallet with private and public key 
    """

    chain = Blockchain()
    wallets = []
    transactions = Transaction()

    def __init__(self):
        pass

    def create_wallet_from_private_key(self, private_key):
        """
        Create a wallet from private key
        """
        pass        

    def generate_private_key(self):
        """
        Generate private key
        """
        return hashlib.sha256(os.urandom(32)).hexdigest()

    def generate_public_key(self):
        """
        Generate public key
        """
        return hashlib.sha256(self.private_key.encode()).hexdigest()

    def get_private_key(self):
        """
        Get private key
        """
        return self.private_key

    def get_public_key(self):
        """
        Get public key
        """
        return self.public_key

    def get_balance(self, address):
        """ Get wallet balance """
        pass

    def create_wallet(self):
        """
        Create a wallet and return the private and public key
        """
        pass