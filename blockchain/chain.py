import hashlib

class BlockChain:
    """ Simple blockchain class """


    def __init__(self):
        self.chain = []

    def create_block(self, proof: int, previous_hash=None):
        """ Create a new block """
        pass

    def hash_block(self, block):
        """ Hash a block """
        pass

    def verify_block(self, block, hash: str):
        """ Verify a block """
        pass

    def get_chain(self):
        """ Get the chain """
        pass

    def get_last_block(self):
        """ Get the last block """
        pass

    def get_last_block_hash(self) -> str:
        """ Get the last block hash """
        pass